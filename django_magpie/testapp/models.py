from django.db import models
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

class ResourceFile(models.Model):
    description = models.CharField(max_length=255)
#Upload to the media root directory 
#(upload_to is the subdir of the media root directory
#TODO: Replace . with user name
    file  = models.FileField(upload_to=".")
    groups = models.ManyToManyField(Group,related_name='rf_groups',blank=True,null=True)
    def __unicode__(self):
        return self.description

class Recommend(models.Model):
    name = models.SlugField(max_length=30, unique=True)
    text = models.CharField(max_length=255)
    pmlLink = models.ForeignKey(ResourceFile, related_name='+',blank=True,null=True)
    videoLink = models.ForeignKey(ResourceFile, related_name='+',blank=True,null=True)
    otherLinks = models.ManyToManyField(ResourceFile,blank=True,null=True,related_name='+')
    def __unicode__(self):
        return self.name

class ExternalLink(models.Model):
    rec = models.ForeignKey(Recommend)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    def __unicode__(self):
        return self.description

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
    (True, 'Yes'),
    (False, 'No')
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
    parent = models.ForeignKey(RuleSet)
    order = models.IntegerField(default=0)
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
        if self.order == 0:
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
    value = models.BooleanField(choices=YN_CHOICES, blank=False, default=False)
    def __unicode__(self):
        return self.variable.name + '=' + val2str(self.value)

class RuleConclusion(models.Model):
    parent = models.ForeignKey(Rule)
    variable = models.ForeignKey(Variable)
    value = models.BooleanField(choices=YN_CHOICES, blank=False, default=False)
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
    def __init__(self, name, text, rank, qa_list):
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
        pass
        
VAR_NODE = 0
REC_NODE = 1

class FactNode(object):

    @staticmethod
    def gen_key(ntype, nid, nvalue):
        return '%d:%d:%d' % (ntype, nid, nvalue)

    def __init__(self, ntype, nid, value, state=NODE_UNTESTED):
        self.node_type = ntype
        self.node_id = nid
        self.value = value
        self.parent_groups = []
        self.children = []
        self.state = state

    def check_state(self, state):
        return self.state == state

    def set_state(self, state):
        self.state = state

    def add_premise(self, group):
        self.parent_groups.append(group)

    def get_premises(self):
        return self.parent_groups

    def add_children(self, child_list):
        for child in child_list:
            self.children.append(child)

    def get_children(self):
        return self.children

    def get_key(self):
        return FactNode.gen_key(self.node_type, self.node_id, self.value)

class FactTree(object):

    def __init__(self):
        self.root_nodes = []
        self.node_dict = {}

    def get_node(self, node_type, fact_id, value):
        key = FactNode.gen_key(node_type, fact_id, value)
        return self.node_dict.get(key, None)

    def get_fact(self, fact_id, value):
        return self.get_node(VAR_NODE, fact_id, value)

    def get_rec(self, rec_id, value):
        return self.get_node(REC_NODE, rec_id, value)

    def get_roots(self):
        return self.root_nodes

    def add_node(self, node):
        key = node.get_key()
        if key not in self.node_dict:
            self.node_dict[key] = node

    def add_root(self, node):
        if node not in self.root_nodes:
            self.root_nodes.append(node)
        self.add_node(node)

    def del_root(self, node):
        if node in self.root_nodes:
            self.root_nodes.remove(node)
        

# rules that fired
# facts that have been tested/established
# recommends given
class Engine(object):

    def __init__(self, ruleset_ids=None, var_list=None, test_ids=None):
        self.ruleset_ids = []
        self.fired_ids = []
        self.var_list = []
        self.test_ids = []
        self.vars_tested = set()
        self.true_facts = set()
        self.test_ids = []
        self.rec_trees = []
        self.debug = False
        # restore state
        if ruleset_ids:
            for rsid in ruleset_ids:
                self.ruleset_ids.append(rsid)
        if var_list:
            self.add_vars(var_list)
        if test_ids:
            for var_id in test_ids:
                self.test_ids.append(var_id)

    # list of ruleset to use
    def get_rulesets(self):
        return self.ruleset_ids

    # list of rule ids that have fired
    def get_fired(self):
        return self.fired_ids

    # return list of variables which has been
    # tested/established/need to be tested
    def get_vars(self):
        return self.var_list

    def get_tests(self):
        return self.test_ids

    def gen_fact_key(self, var_id, value):
        return '%d:%d' % (var_id, value)

    def create_vnode(self, var_id, value):
        key = self.gen_fact_key(var_id, value)
        if key in self.true_facts:
            state = NODE_PASSED
        elif var_id in self.vars_tested:
            state = NODE_TESTED
        else:
            state = NODE_UNTESTED
        return FactNode(VAR_NODE, var_id, value, state)

    def get_questions(self):
        questions = []
        for variable in Variable.objects.filter(id__in=self.test_ids):
            if variable.ask:
                questions.append(variable)
        return questions

    # return list of recommendation for rules that have fired
    def get_recommends(self):
        recommends = []
        recommend_ids = []
        # TODO order by rank
        for rec_tree in self.rec_trees:
            for rnode in  rec_tree.get_roots():
                recommend_ids.append(rnode.node_id)
        for recommend in Recommend.objects.filter(id__in=recommend_ids):
            recommends.append(recommend)
        return recommends

    #Return list of recommendations that have been ruled out
    def getNonRecommended(self):
        non_recommended = []
        return non_recommended

    def get_answers(self):
        return []

    def next_premises(self, search_premises, qa_list, node_set):
        if len(search_premises) == 0:
            return
        tnode_list = []
        for tnode in search_premises[0].get_nodes():
            if tnode.node_id not in node_set:
                var = Variable.objects.get(pk=tnode.node_id)
                qa = (var.name, tnode.value)
                qa_list.append(qa)
                tnode_list.append(tnode)
                node_set.add(tnode.node_id)
        for tnode in tnode_list:
            self.next_premises(tnode.get_premises(), qa_list, node_set)

    def get_reasons(self):
        # first get unique list of recommends nodes
        rdict = {}
        for rec_tree in self.rec_trees:
            for rnode in rec_tree.get_roots():
                if rnode.node_id in rdict:
                    # replace only if node has higher rank
                    onode = rdict[rnode.node_id]
                    if rnode.value > onode.value:
                        rdict[rnode.node_id] = rnode
                else:
                    rdict[rnode.node_id] = rnode
    
        reasons = []
        for rnode in rdict.values():
            qa_list = []
            node_set = set()
            self.next_premises(rnode.get_premises(), qa_list, node_set)
            recommend = Recommend.objects.get(pk=rnode.node_id)
            reasons.append(Reason(
                    recommend.name,
                    recommend.text, 
                    rnode.value, 
                    qa_list))

        return sorted(reasons, key=lambda reason: reason.rank, reverse=True)
        
    def getNonReasons(self):
        reasons = []
        return reasons
        
    def getUnansweredReasons(self):
        reasons = []
        return reasons

    # asserted fact = variable that has been assinged a value
    def add_var(self, var_id, value):
        if var_id not in self.vars_tested:
            self.vars_tested.add(var_id)
        if value != None:
            # we got an answer
            key = self.gen_fact_key(var_id, value)
            if key not in self.true_facts:
                self.var_list.append((var_id, value))
                self.true_facts.add(key)

    def add_vars(self, facts):
        for item in facts:
            self.add_var(item[0], item[1])

    def add_consequent(self, rule):
        if self.debug: print 'rule=', rule
        for conclusion in rule.ruleconclusion_set.all():
            if self.debug: print 'conclusion=', conclusion
            self.add_var(conclusion.variable_id, conclusion.value)
        for rrecommend in rule.rulerecommend_set.all():
            if self.debug: print 'recommend=', rrecommend

    def add_recommends(self, rule, tree):
        premise_group = FactGroup()
        for premise in rule.rulepremise_set.all():
            node = tree.get_fact(premise.variable_id, premise.value)
            if not node:
                node = self.create_vnode(premise.variable_id, premise.value)
                tree.add_node(node)
            premise_group.add_node(node)

        for conclusion in rule.ruleconclusion_set.all():
            node = tree.get_fact(conclusion.variable_id, conclusion.value)
            if not node:
                node = self.create_vnode(conclusion.variable_id, conclusion.value)
                tree.add_node(node)
            node.add_premise(premise_group)

        for rrecommend in rule.rulerecommend_set.all():
            node = tree.get_rec(rrecommend.recommend_id, rrecommend.rank)
            if not node:
                node = FactNode(REC_NODE, 
                    rrecommend.recommend_id, 
                    rrecommend.rank, 
                    NODE_PASSED)
                tree.add_root(node)
                node.add_premise(premise_group)

    def premise_fired(self, rule):
        for premise in rule.rulepremise_set.all():
            key = self.gen_fact_key(premise.variable_id, premise.value)
            if key not in self.true_facts:
                return False
        return True

    def find_tests(self, tree):
        # now find next set of variables to test
        loop_check = set()
        test_ids = []
        search_nodes = tree.get_roots()
        while len(search_nodes) > 0:
            next_search = []
            for node in search_nodes:
                if node.state == NODE_UNTESTED:
                    test_ids.append(node.node_id)
                elif node.state == NODE_PASSED:
                    for child in node.get_children():
                        # only one of the child premise groups has to be true (OR logic)
                        for group in child.get_premises():
                            if group.all_passed() and child.node_id not in loop_check:
                                next_search.append(child)
                                loop_check.add(child.node_id)
                                break
            if len(test_ids) == 0:
                search_nodes = next_search
            else:
                search_nodes = []

        # remember for later
        self.test_ids.extend(test_ids)
    
    # upside down truth tree (roots are the recommends)
    def build_ttree(self, ruleset):
        tree = FactTree()
        for rule in ruleset.rule_set.all():
            if self.premise_fired(rule):
                premise_group = FactGroup()
                for premise in rule.rulepremise_set.all():
                    node = tree.get_fact(premise.variable_id, premise.value)
                    if not node:
                        node = self.create_vnode(premise.variable_id, premise.value)
                        tree.add_node(node)
                for conclusion in rule.ruleconclusion_set.all():
                    node = tree.get_fact(conclusion.variable_id, conclusion.value)
                    if not node:
                        node = self.create_vnode(conclusion.variable_id, conclusion.value)
                        tree.add_node(node)
                    node.add_premise(premise_group)
                for rrecommend in rule.rulerecommend_set.all():
                    node = tree.get_rec(rrecommend.recommend_id, 0)
                    if not node:
                        node = FactNode(NODE_REC, 
                                    rrecommend.recommend_id, 
                                    rrecommend.rank, 
                                    NODE_PASSED)
                        tree.add_root(node)
                    node.add_premise(premise_group)
        return tree

    # build and-or tree (roots are the facts)
    def build_aotree(self, ruleset):
        tree = FactTree()
        for rule in ruleset.rule_set.exclude(id__in=self.fired_ids):
            premise_group = FactGroup()
            for premise in rule.rulepremise_set.all():
                node = tree.get_fact(premise.variable_id, premise.value)
                if not node:
                    node = self.create_vnode(premise.variable_id, premise.value)
                    tree.add_root(node)
                premise_group.add_node(node)
            premise_group.check_fail()
            conclusion_nodes = []
            for conclusion in rule.ruleconclusion_set.all():
                node = tree.get_fact(conclusion.variable_id, conclusion.value)
                if not node:
                    node = self.create_vnode(conclusion.variable_id, conclusion.value)
                    tree.add_node(node)
                node.add_premise(premise_group)
                tree.del_root(node)
                conclusion_nodes.append(node)
            for node in premise_group.get_nodes():
                node.add_children(conclusion_nodes)
        return tree

    def forward_chain(self, ruleset):
        new_facts = True 
        fired_ids = []
        tree = FactTree()
        # now look for rules that have fired
        while new_facts:
            new_facts = False
            for rule in ruleset.rule_set.exclude(id__in=fired_ids):
                if self.premise_fired(rule):
                    self.add_consequent(rule)
                    self.add_recommends(rule, tree)
                    fired_ids.append(rule.id)
                    new_facts = True
        self.fired_ids.extend(fired_ids)
        self.rec_trees.append(tree)

    # given some answers update facts base and check if rules have fired
    # we use forward chaining here
    # answers = list of (var_id,value) tuples
    def next_state(self, answers=None):
        # first add asserted facts
        if answers:
            self.add_vars(answers)
        # now add variables for which we did not get answers
        for var_id in self.test_ids:
            self.add_var(var_id,None)
        # and reset testable node list
        self.test_ids = []
        # reset rule list
        self.fire_ids = []
        self.rec_trees = []

        for ruleset in RuleSet.objects.filter(id__in=self.ruleset_ids):
            self.forward_chain(ruleset)
            tree = self.build_aotree(ruleset)
            self.find_tests(tree)

def state_encode(state):
    sdict = {}
    sdict['rulesets'] = state.get_rulesets()
    sdict['vars'] = state.get_vars()
    sdict['tests'] = state.get_tests()
    return sdict.items()

def state_decode(slist):
    sdict = dict(slist)
    ruleset_ids = sdict.get('rulesets', None)
    var_list = sdict.get('vars', None)
    test_ids = sdict.get('tests', None)
    return Engine(ruleset_ids, var_list, test_ids)

def start_state(user):
    ruleset_ids = []
    for ruleset in RuleSet.objects.all():
        ruleset_ids.append(ruleset.id)
    return Engine(ruleset_ids)