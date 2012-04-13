from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from register.models import Profile
from utils import OrderedDict

def userPath(instance, filename):
    return filename
        
class ResourceFile(models.Model):
    description = models.CharField(max_length=255)
    file  = models.FileField(upload_to=userPath)
    restricted = models.BooleanField()
    restricted_to = models.ManyToManyField(User,blank=True,null=True,related_name='+')
    owner = models.ForeignKey(User,blank=True,null=True)
    class Meta:
        permissions = (
            ("restricted_access", "Can access restricted files"),
        )
    
    def __unicode__(self):
        return self.description    

class Recommend(models.Model):
    name = models.SlugField(max_length=30, unique=True)
    text = models.CharField(max_length=255)
    pmlLink = models.ForeignKey(ResourceFile, related_name='+',blank=True,null=True)
    videoLink = models.ForeignKey(ResourceFile, related_name='+',blank=True,null=True)
    otherLinks = models.ManyToManyField(ResourceFile,blank=True,null=True,related_name='+')
    def __unicode__(self):
        return self.text
        
class ExternalLink(models.Model):
    rec = models.ForeignKey(Recommend)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    def __unicode__(self):
        return self.description


#BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
        
class RecsSummary(object): 
    def __init__(self, text, details, pmlPath, vidLink):
        self.text = text
        self.links = details
        self.pmlPath = pmlPath
        self.vidLink = vidLink    
     
#Pack together the recommendation data in a nice way.        
def recSummaryClosure(user):
    restrictedAccess = user.is_staff or user.is_superuser or user.has_perm('knowledge.restricted_access')
    def getRecSummary(rec):
        recsList = []
        pmlPath = None
        vidLink = None
        if rec.videoLink != None and (not rec.videoLink.restricted or restrictedAccess or user in rec.videoLink.restricted_to.all()):
            vidLink = rec.videoLink.file.url
        if rec.pmlLink != None and (not rec.pmlLink.restricted or restrictedAccess  or user in rec.pmlLink.restricted_to.all()):
            recsList.append(("PML XML Link", rec.pmlLink.file.url))
            pmlPath = rec.pmlLink.file.name
        for others in rec.otherLinks.all():
            if (not others.restricted or restrictedAccess  or user in others.restricted_to.all()):
                recsList.append((others.description,others.file.url))
        for link in ExternalLink.objects.filter(rec=rec.id):
            recsList.append((link.description,link.link))
        return RecsSummary(rec.text,recsList,pmlPath,vidLink)
    return getRecSummary

class Variable(models.Model):
    name = models.SlugField(max_length=30, unique=True)
    ask = models.BooleanField(default=True)
    prompt = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class VariableChoice(models.Model):
    parent = models.ForeignKey(Variable)
    value = models.CharField(max_length=100)
    def __unicode__(self):
        return self.value

YN_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No')
)

def val2str(val):
    if type(val) is bool:
        return 'Yes' if val else 'No'
    return str(val)

class RuleSet(models.Model):
    name = models.SlugField(max_length=30, unique=True)
    def __unicode__(self):
        return self.name

class Rule(models.Model):
    parent = models.ForeignKey(RuleSet, editable=False)
    order = models.PositiveIntegerField(default=0)
    def get_dets(self):
        tostr = lambda names: ' AND '.join(names)
        pnames = []
        for premise in self.rulepremise_set.all():
            pnames.append(str(premise))
        cnames = []
        for conclusion in self.ruleconclusion_set.all():
            cnames.append(str(conclusion))
        for recommend in self.rulerecommend_set.all():
            cnames.append(str(recommend))
        return "IF %s THEN %s" % (tostr(pnames), ','.join(cnames))

    def save(self, *args, **kwargs):
        # ensure the order is set and unique
        if self.pk is None:
            qset = Rule.objects.filter(parent=self.parent).aggregate(models.Max('order'))
            try:
                self.order = qset['order__max'] + 1
            except TypeError:
                self.order = 1
        super(Rule, self).save(*args, **kwargs) 
    
    def __unicode__(self):
        return self.get_dets()

    class Meta:
        ordering = ('order',)


class RulePremise(models.Model):
    parent = models.ForeignKey(Rule)
    variable = models.ForeignKey(Variable)
    value = models.CharField(max_length=1,choices=YN_CHOICES, default='N')
    def __unicode__(self):
        return self.variable.name + '=' + val2str(self.value)

class RuleConclusion(models.Model):
    parent = models.ForeignKey(Rule)
    variable = models.ForeignKey(Variable)
    value = models.CharField(max_length=1,choices=YN_CHOICES, default='N')
    def __unicode__(self):
        return self.variable.name + '=' + val2str(self.value)

class RuleRecommend(models.Model):
    parent = models.ForeignKey(Rule)
    recommend = models.ForeignKey(Recommend)
    rank = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.recommend)

def get_ids(alist):
    return map(lambda elem:elem.id, alist)

class Reason(object):
    def __init__(self, rid, name, text, rank, qa_list):
        self.rid = rid
        self.name = name
        self.text = text
        self.rank = rank
        self.qa_list = qa_list



NODE_UNTESTED = 0
NODE_TESTED = 1
NODE_PASSED = 2

class FactGroup(object):

    def __init__(self):
        self.nodes = []
        self.children = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def all_passed(self):
        for node in self.nodes:
            if not node.check_state(NODE_PASSED):
                return False
        return True

    def check_fail(self):
        for node in self.nodes:
            if node.check_state(NODE_TESTED):
                return True
        return False

    def del_root(self, tree):
        for node in self.nodes:
            tree.del_root(node)
            if node.check_state(NODE_UNTESTED):
                node.set_state(NODE_TESTED)

    def add_children(self, child_list):
        for child in child_list:
            self.children.append(child)

    def get_children(self):
        return self.children

    def __str__(self):
        alist = []
        for node in self.nodes:
            alist.append(str(node))
        return '[' +  ','.join(alist) + ']'
        
VAR_NODE = 0
REC_NODE = 1

class FactNode(object):

    @staticmethod
    def gen_key(ntype, nid, nvalue):
        return '%d:%d:%s' % (ntype, nid, nvalue)

    def __init__(self, ntype, nid, value, state=NODE_UNTESTED):
        self.node_type = ntype
        self.node_id = nid
        self.value = value
        self.parent_groups = []
        self.state = state
        self.level = 0

    def get_type(self):
        return self.node_type

    def check_state(self, state):
        return self.state == state

    def set_state(self, state):
        self.state = state

    def get_level(self):
        return self.level

    def add_premise(self, group):
        self.parent_groups.append(group)

    def get_premises(self):
        return self.parent_groups

    def set_premises(self, premises):
        self.parent_groups = premises


    def gen_fact_key(self):
        return '%d:%s' %( self.node_id, self.node_value)

    def get_key(self):
        return FactNode.gen_key(self.node_type, self.node_id, self.value)

    def __str__(self):
        return self.get_key()

class FactTree(object):

    def __init__(self):
        self.groups = []
        self.goals = []
        self.node_dict = {}

    def get_node(self, node_type, fact_id, value):
        key = FactNode.gen_key(node_type, fact_id, value)
        return self.node_dict.get(key, None)

    def get_fact(self, fact_id, value):
        return self.get_node(VAR_NODE, fact_id, value)

    def get_rec(self, rec_id, value):
        return self.get_node(REC_NODE, rec_id, value)

    def get_level(self, level):
        item_list = []
        if len(self.levels) >= level:
            item_set = self.levels[level-1]
            for item in item_set:
                item_list.append(item)
        return item_list

    def get_maxlevel(self):
        return len(self.levels)

    def get_roots(self):
        return self.get_level(1)

    def add_node(self, node):
        key = node.get_key()
        self.node_dict[key] = node

    def add_fact(self, node):
        self.add_node(node)

    def add_rec(self, node):
        self.add_node(node)
        self.goals.append(node)

    def add_root(self, node):
        self.add_node(node)
        self.level_node(node, 1)

    def del_root(self, node):
        if node.level == 1:
            self.unlevel_node(node)

    def add_group(self, group):
        self.groups.append(group)
    
    def get_groups(self):
        return self.groups

    def get_goals(self):
        return self.goals


# FACT STATE (where it came from)
FACT_ASSERTED = 0
FACT_ANSWERED = 1
FACT_INFERRED = 2

# rules that fired
# facts that have been tested/established
# recommends given
class Engine(object):

    def __init__(self, ruleset_ids=None, var_list=None, test_ids=None):
        self.ruleset_ids = []
        self.test_ids = []
        self.fact_state =  OrderedDict()
        self.rec_nodes = []
        self.debug = False
        # restore state
        if ruleset_ids:
            for rsid in ruleset_ids:
                self.ruleset_ids.append(rsid)
        if var_list:
            self.add_vars(var_list, FACT_ASSERTED)
        if test_ids:
            for var_id in test_ids:
                self.test_ids.append(var_id)

    # list of ruleset to use
    def get_rulesets(self):
        return self.ruleset_ids

    # return list of variables which has been
    # tested/established/need to be tested
    def get_vars(self, need_state=False):
        var_list = []
        for key, state in self.fact_state.items():
            vid,value = self.decode_fact_key(key)
            if need_state:
                var_list.append((vid,value,state))
            else:
                var_list.append((vid,value))
        return var_list

    def get_tests(self):
        return self.test_ids

    def gen_fact_key(self, var_id, value):
        return '%d:%s' % (var_id, value)

    def decode_fact_key(self, key):
        idstr,value = key.split(':',1)
        var_id = int(idstr)
        return var_id,value

    def create_vnode(self, var_id, value):
        key = self.gen_fact_key(var_id, value)
        if key in self.fact_state:
            state = NODE_PASSED
        elif self.gen_fact_key(var_id,'') in self.fact_state:
            state = NODE_TESTED
        else:
            state = NODE_UNTESTED
        return FactNode(VAR_NODE, var_id, value, state)

    def get_unique_rnodes(self):
        # first get unique list of recommends nodes
        rdict = {}
        for rnode in self.rec_nodes:
            if rnode.node_id in rdict:
                # replace only if node has higher rank
                onode = rdict[rnode.node_id]
                if rnode.value > onode.value:
                    rdict[rnode.node_id] = rnode
            else:
                rdict[rnode.node_id] = rnode
        return rdict.values()
        
    def getPriorQuestions(self, answers):
        questions = []
        questionAns = []
        for ans in answers:
            if Variable.objects.filter(id=ans[0])[0].ask:
                questions.append(Variable.objects.filter(id=ans[0])[0])
                questionAns.append(ans[1])
        return zip(questions,questionAns)

    def get_questions(self):
        questions = []
        for variable in Variable.objects.filter(id__in=self.test_ids):
            if variable.ask:
                questions.append(variable)
        return questions

    # return list of recommendation for rules that have fired
    # TODO fix views to use only get_reasons call
    def get_recommends(self):
        rnodes = self.get_unique_rnodes()
        recommends = []
        for rnode in rnodes:
            recommend = Recommend.objects.get(pk=rnode.node_id)
            # FIXME - this is a hack
            recommend.rank = rnode.value
            recommends.append(recommend)

        return sorted(recommends, key=lambda recommend: recommend.rank, reverse=True)

    def get_answers(self):
        answers = []
        for key, state in self.fact_state.items():
            if state == FACT_ANSWERED:
                vid,value = self.decode_fact_key(key)
                # TODO should we include questions not answered
                if value:
                    answers.append((vid,value))
        return answers

    # reverse climb the tree to the top node (we use node_set to prevent loops)
    def next_premises(self, search_premises, qa_list, node_set):
        if len(search_premises) == 0:
            return
        tnode_list = []
        for tnode in reversed(search_premises[0].get_nodes()):
            if tnode not in node_set:
                var = Variable.objects.get(pk=tnode.node_id)
                # FIXME this really should be the fact name
                text = var.prompt if len(var.prompt) > 0 else var.name
                qa = (text, tnode.value)
                qa_list.append(qa)
                tnode_list.append(tnode)
                node_set.add(tnode)
        for tnode in tnode_list:
            self.next_premises(tnode.get_premises(), qa_list, node_set)

    def get_reasons(self):
        # first get unique list of recommends nodes
        rnode_list = self.get_unique_rnodes()
        # now build a list of the reasons that go with them
        reasons = []
        for rnode in rnode_list:
            qa_list = []
            node_set = set()
            self.next_premises(rnode.get_premises(), qa_list, node_set)
            recommend = Recommend.objects.get(pk=rnode.node_id)
            reasons.append(Reason(
                    recommend.id,
                    recommend.name,
                    recommend.text, 
                    rnode.value, 
                    qa_list))

        return sorted(reasons, key=lambda reason: reason.rank, reverse=True)

    # asserted fact = variable that has been assinged a value
    def add_var(self, var_id, value, state):
        # record that we've seen this variable
        key = self.gen_fact_key(var_id, value)
        if key not in self.fact_state:
            self.fact_state[key] = state
        else:
            # ASSERTED < ANSWERED < INFERRED
            curr_state = self.fact_state[key]
            if state < curr_state:
                self.fact_state[key] = state

    def add_vars(self, facts, default_state):
        for item in facts:
            state = item[2] if len(item) > 2 else default_state
            self.add_var(item[0], item[1], state)

    def build_tree(self, ruleset):
        tree = FactTree()
        for rule in ruleset.rule_set.all():
            premise_group = FactGroup()
            for premise in rule.rulepremise_set.all():
                node = tree.get_fact(premise.variable_id, premise.value)
                if not node:
                    node = self.create_vnode(premise.variable_id, premise.value)
                    tree.add_fact(node)
                premise_group.add_node(node)
            conclusion_nodes = []
            for conclusion in rule.ruleconclusion_set.all():
                node = tree.get_fact(conclusion.variable_id, conclusion.value)
                if not node:
                    node = self.create_vnode(conclusion.variable_id, conclusion.value)
                    tree.add_fact(node)
                node.add_premise(premise_group)
                conclusion_nodes.append(node)
            recommend_nodes = [] 
            for rrecommend in rule.rulerecommend_set.all():
                node = tree.get_rec(rrecommend.recommend_id, rrecommend.rank)
                if not node:
                    node = FactNode(REC_NODE, 
                        rrecommend.recommend_id, 
                        rrecommend.rank, 
                        NODE_UNTESTED)
                    tree.add_rec(node)
                node.add_premise(premise_group)
                recommend_nodes.append(node)
            premise_group.add_children(conclusion_nodes)
            premise_group.add_children(recommend_nodes)
            tree.add_group(premise_group)
        return tree

    def forward_chain(self, tree):
        # now look for rules that have fired
        test_groups = tree.get_groups()
        new_facts = True
        while new_facts:
            new_facts = False
            next_test = []
            for group in test_groups:
                if group.all_passed():
                    for child in group.get_children():
                        child.set_state(NODE_PASSED)
                        if child.get_type() == VAR_NODE:
                            self.add_var(child.node_id, 
                                child.value, 
                                FACT_INFERRED)
                    new_facts = True
                else:
                    next_test.append(group)
            test_groups = next_test
        return test_groups

    def get_first(self, premise_list, node_set):
        if self.debug:
            print 'get_first premise', [ str(x) for x in premise_list]
        for premise in premise_list:
            num_loop = 0
            for node in premise.get_nodes():
                if self.debug: print 'node', node
                if node in node_set:
                    if self.debug: print '+++++++LOOP++++++++'
                    num_loop += 1
                    continue
                node_set.add(node)
                if node.check_state(NODE_UNTESTED):
                    leafp = self.get_first(node.get_premises(), node_set)
                    if leafp:
                        return leafp
            if num_loop == 0:
                return premise
        return None

    def find_backchains(self, node, node_set):
        if self.debug: print 'find_backchains', node
        backchains = []
        if node in node_set:
            if self.debug: print '+++++++LOOP++++++++'
            #print 'Node', node, 'premises', [ str(x) for x in node_set ]
            return True
        node_set.add(node)
        #print 'Node', node, 'premises', [ str(x) for x in node.get_premises() ]
        for premise in node.get_premises():
            if self.debug: print 'premise', premise
            untested = []
            num_tested = 0
            for pnode in premise.get_nodes():
                if pnode.check_state(NODE_UNTESTED):
                    untested.append(pnode)
                elif pnode.check_state(NODE_TESTED):
                    num_tested = num_tested + 1
            if num_tested == 0 and len(untested) > 0:
                num_backchain = 0
                for pnode in untested:
                    if self.find_backchains(pnode, node_set):
                        num_backchain += 1
                if self.debug: print 'num_backchain', num_backchain, len(untested)
                if num_backchain == len(untested):
                    if self.debug: print 'backchain', premise
                    backchains.append(premise)
        if self.debug: 
            print 'Node', node, 'backchains', [ str(x) for x in backchains ]
        premsies = node.get_premises()
        node.set_premises(backchains)
        return len(premsies) == 0 or len(backchains) > 0
    
    def find_goals(self, tree, unfired):
        test_premises = []
        for rec_node in tree.get_goals():
            if rec_node.check_state(NODE_PASSED):
                if self.debug: print 'Found goal!', rec_node
                self.rec_nodes.append(rec_node)
            else:
                if self.find_backchains(rec_node, set()):
                    premises = rec_node.get_premises()
                    test_premises.append(self.get_first(premises, set()))
        test_ids = []
        for premise in test_premises: 
            for node in premise.get_nodes():
                if node.state == NODE_UNTESTED:
                    variable = Variable.objects.get(pk=node.node_id)
                    if variable.ask:
                        test_ids.append(node.node_id)
        if len(test_ids) > 0:
            self.test_ids.append(test_ids[0])
                
    # given some answers update facts base and check if rules have fired
    # we use forward chaining here
    # answers = list of (var_id,value) tuples
    def next_state(self, answers=None):
        # first add asserted facts
        answer_ids = set()
        if answers:
            if self.debug: print 'Got answers', answers
            self.add_vars(answers, FACT_ANSWERED)
            for item in answers:
                answer_ids.add(item[0])
        # now add variables for which we did not get answers
        for var_id in self.test_ids:
            if var_id not in answer_ids:
                self.add_var(var_id, '', FACT_ANSWERED)

        # and reset testable node list
        self.test_ids = []
        # reset rule list
        self.fire_ids = []
        # this really needs to be fixed
        self.rec_nodes = []

        for ruleset in RuleSet.objects.filter(id__in=self.ruleset_ids):
            tree = self.build_tree(ruleset)
            unfired = self.forward_chain(tree)
            self.find_goals(tree, unfired)


def state_encode(state):
    sdict = {}
    sdict['rulesets'] = state.get_rulesets()
    sdict['vars'] = state.get_vars(True)
    sdict['tests'] = state.get_tests()
    return sdict.items()
def state_decode(slist):
    sdict = dict(slist)
    ruleset_ids = sdict.get('rulesets', None)
    var_list = sdict.get('vars', None)
    test_ids = sdict.get('tests', None)
    return Engine(ruleset_ids, var_list, test_ids)

class FactStart(object):

    def __init__(self):
        self.rulesets = []
        self.facts = []

    def add_ruleset(self, ruleset):
        if ruleset and ruleset not in self.rulesets:
            self.rulesets.append(ruleset)

    def add_facts(self, facts):
        self.facts.extend(facts)

    def get_guest_profile(self):
        if not settings.GUEST_PROFILE:
            return None

        try:
            profile = Profile.objects.get(name=settings.GUEST_PROFILE)
        except Profile.DoesNotExist:
            profile = None

        return profile

    def get_user_profile(self, user):
        account = user.get_profile()
        return account.profile

    def get_profile(self, user):
        if user.is_authenticated():
            profile = self.get_user_profile(user)
            if not profile:
                # try the guest instead
                profile = self.get_guest_profile()
        else:
            profile = self.get_guest_profile()
        return profile

    def load_profile(self, user):
        profile = self.get_profile(user)
        if profile:
            self.add_ruleset(profile.ruleset)
            self.add_facts(profile.get_answers())

    def get_facts(self):
        return self.facts

    def get_ruleset_ids(self):
        ruleset_ids = []
        for ruleset in self.rulesets:
            ruleset_ids.append(ruleset.id)
        return ruleset_ids

def start_state(user):
    start = FactStart()
    start.load_profile(user)
    return Engine(start.get_ruleset_ids(), start.get_facts())
