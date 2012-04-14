from django.test import TestCase
from models import *
from views import get_answers
from django.contrib.auth.models import User
from register.models import Profile,Account
from templatetags.customFilters import *

# dummy class used for tests
class TestModel:
    def __init__(self, id):
        self.id = id

class ParserTests(TestCase):

    def setUp(self):
        self.parser = PremiseParser()

    def testEmpty(self):
        pos = -1
        got_except = False
        try:
            self.parser.parse([])
        except PremiseException as e:
            got_except = True
            pos = e.pos
        self.assertTrue(got_except and pos == 0)

    def testSimple(self):
        premise = RulePremise(
                lchoice='', 
                variable=Variable(id=100,name='x'),
                value='Y',
                rchoice='')
        root = self.parser.parse([premise])
        self.assertTrue(root.ptype==PTYPE_VAR and 
              root.left == 100 and
              root.right == 'Y')

    def testSimple1Compound(self):
        premise = RulePremise(
                lchoice='(', 
                variable=Variable(id=100,name='x'),
                value='Y',
                rchoice=')')
        root = self.parser.parse([premise])
        self.assertTrue(root.ptype==PTYPE_VAR and 
              root.left == 100 and
              root.right == 'Y')

    def testSimple2Compound(self):
        premise = RulePremise(
                lchoice='((', 
                variable=Variable(id=100,name='x'),
                value='Y',
                rchoice='))')
        root = self.parser.parse([premise])
        self.assertTrue(root.ptype==PTYPE_VAR and 
              root.left == 100 and
              root.right == 'Y')

    def testAnd1(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        plist = [
            RulePremise(variable=x, value='Y', rchoice='&'),
            RulePremise(variable=y, value='Y', rchoice='')
        ]
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_AND)
        left = root.left
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')
        right = root.right
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')

    def testAnd1CompoundAll(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        plist = [
            RulePremise(lchoice='(',variable=x, value='Y', rchoice='&'),
            RulePremise(variable=y, value='Y', rchoice=')')
        ]
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_AND)
        left = root.left
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')
        right = root.right
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')

    def testAnd1CompoundEach(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        plist = [
            RulePremise(lchoice='(',variable=x, value='Y', rchoice=') &'),
            RulePremise(lchoice='(', variable=y, value='Y', rchoice=')')
        ]
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_AND)
        left = root.left
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')
        right = root.right
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')

    def testAnd2(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        z = Variable(id=102,name='z')
        plist = [
            RulePremise(variable=x, value='Y', rchoice='&'),
            RulePremise(variable=y, value='Y', rchoice='&'),
            RulePremise(variable=z, value='Y', rchoice='')
        ]
        # should be (x&y) & z
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_AND)
        # check right (z)
        node = root.right
        self.assertTrue(node.ptype ==PTYPE_VAR and 
              node.left == z.id and
              node.right == 'Y')
        # check left (x&y)
        node = root.left
        self.assertEquals(node.ptype, PTYPE_AND)
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.left.left == x.id and
              node.left.right == 'Y')
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.right.left == y.id and
              node.right.right == 'Y')

    def testAnd2CompoundAll(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        z = Variable(id=102,name='z')
        plist = [
            RulePremise(lchoice='(',variable=x, value='Y', rchoice='&'),
            RulePremise(variable=y, value='Y', rchoice='&'),
            RulePremise(variable=z, value='Y', rchoice=')')
        ]
        # should be (x&y) & z
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_AND)
        # check right (z)
        node = root.right
        self.assertTrue(node.ptype ==PTYPE_VAR and 
              node.left == z.id and
              node.right == 'Y')
        # check left (x&y)
        node = root.left
        self.assertEquals(node.ptype, PTYPE_AND)
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.left.left == x.id and
              node.left.right == 'Y')
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.right.left == y.id and
              node.right.right == 'Y')

    def testAnd2CompoundeEach(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        z = Variable(id=102,name='z')
        plist = [
            RulePremise(lchoice='(',variable=x, value='Y', rchoice=') & ('),
            RulePremise(variable=y, value='Y', rchoice=') & ('),
            RulePremise(variable=z, value='Y', rchoice=')')
        ]
        # should be (x&y) & z
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_AND)
        # check right (z)
        node = root.right
        self.assertTrue(node.ptype ==PTYPE_VAR and 
              node.left == z.id and
              node.right == 'Y')
        # check left (x&y)
        node = root.left
        self.assertEquals(node.ptype, PTYPE_AND)
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.left.left == x.id and
              node.left.right == 'Y')
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.right.left == y.id and
              node.right.right == 'Y')

    def test1Or(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        plist = [
            RulePremise(variable=x, value='Y', rchoice='|'),
            RulePremise(variable=y, value='Y', rchoice='')
        ]
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_OR)
        left = root.left
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')
        right = root.right
        self.assertTrue(left.ptype ==PTYPE_VAR and 
              left.left == x.id and
              left.right == 'Y')

    def test2Or(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='x')
        z = Variable(id=102,name='z')
        plist = [
            RulePremise(variable=x, value='Y', rchoice='|'),
            RulePremise(variable=y, value='Y', rchoice='|'),
            RulePremise(variable=z, value='Y', rchoice='')
        ]
        # should be (x|y) | z
        root = self.parser.parse(plist)
        self.assertEquals(root.ptype, PTYPE_OR)
        # check right (z)
        node = root.right
        self.assertTrue(node.ptype ==PTYPE_VAR and 
              node.left == z.id and
              node.right == 'Y')
        # check left (x&y)
        node = root.left
        self.assertEquals(node.ptype, PTYPE_OR)
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.left.left == x.id and
              node.left.right == 'Y')
        self.assertTrue(node.left.ptype ==PTYPE_VAR and 
              node.right.left == y.id and
              node.right.right == 'Y')

class DNFTests(TestCase):
    
    def setUp(self):
        self.parser = PremiseParser()

    def test_grab_or_nodes(self):
        # none
        or_list = []
        grab_or_nodes(None, or_list)
        self.assertTrue(len(or_list) == 0)
        # 1 var
        node = PremiseNode(PTYPE_VAR, 100, 'Y')
        grab_or_nodes(node, or_list)
        self.assertTrue(len(or_list) == 1 and or_list[0] == node)
        # 1 and
        or_list = []
        lnode = PremiseNode(PTYPE_VAR, 100, 'Y')
        rnode = PremiseNode(PTYPE_VAR, 101, 'Y')
        node = PremiseNode(PTYPE_AND, lnode, rnode)
        grab_or_nodes(node, or_list)
        self.assertTrue(len(or_list) == 1)
        self.assertTrue(or_list[0] == node)
        # 1 or
        or_list = []
        lnode = PremiseNode(PTYPE_AND, 100, 'Y')
        rnode = PremiseNode(PTYPE_AND, 101, 'Y')
        node = PremiseNode(PTYPE_OR, lnode, rnode)
        grab_or_nodes(node, or_list)
        self.assertTrue(len(or_list) == 2)
        self.assertTrue(or_list[0] == lnode)
        self.assertTrue(or_list[1] == rnode)

    def test_treecmp(self):
        node1 = PremiseNode(PTYPE_VAR, 100, 'Y')
        node1_copy =  PremiseNode(PTYPE_VAR, 100, 'Y')
        node2 = PremiseNode(PTYPE_VAR, 101, 'Y')
        self.assertTrue(treecmp(None, None))
        self.assertTrue(treecmp(node1, node1))
        self.assertTrue(treecmp(node1, node1_copy))


    def test_simple(self):
        x = Variable(id=100,name='x')
        plist = [RulePremise(variable=x, value='Y')]
        # create root
        root = self.parser.parse(plist)
        root = wff_dnf(root)
        self.assertTrue(root.ptype==PTYPE_VAR and 
              root.left == 100 and
              root.right == 'Y')

    def test_case1(self):
        x = Variable(id=100,name='x')
        y = Variable(id=101,name='y')
        z = Variable(id=102,name='z')

        plist1 = [
            RulePremise(variable=x, value='Y', rchoice='&'),
            RulePremise(lchoice='(', variable=y, value='Y', rchoice='|'),
            RulePremise(variable=z, value='Y', rchoice=')')
        ]
        root1 = self.parser.parse(plist1)
        root1 = wff_dnf(root1)
        
        plist2 = [
            RulePremise(lchoice='(', variable=x, value='Y', rchoice='&'),
            RulePremise(variable=y, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=x, value='Y', rchoice='&'),
            RulePremise(variable=z, value='Y', rchoice=')')
        ]
        root2 = self.parser.parse(plist2)

        self.assertTrue(treecmp(root1, root2))

    def test_case2(self):

        x = Variable(id=100,name='x')
        y = Variable(id=101,name='y')
        z = Variable(id=102,name='z')

        plist1 = [
            RulePremise(variable=x, value='Y', rchoice='&'),
            RulePremise(lchoice='(', variable=y, value='Y', rchoice='&'),
            RulePremise(variable=z, value='Y', rchoice=')')
        ]
        root1 = self.parser.parse(plist1)
        wff_dnf(root1)
        
        plist2 = [
            RulePremise(lchoice='(', variable=x, value='Y', rchoice='&'),
            RulePremise(variable=y, value='Y', rchoice=') &'),
            RulePremise(variable=z, value='Y')
        ]
        root2 = self.parser.parse(plist2)

        self.assertTrue(treecmp(root1, root2))

    def test_case3(self):

        x = Variable(id=100,name='x')
        y = Variable(id=101,name='y')
        z = Variable(id=102,name='z')

        plist1 = [
            RulePremise(lchoice='(', variable=x, value='Y', rchoice='|'),
            RulePremise(variable=y, value='Y', rchoice=') &'),
            RulePremise(variable=z, value='Y')
        ]
        root1 = self.parser.parse(plist1)
        wff_dnf(root1)
        
        plist2 = [
            RulePremise(lchoice='(', variable=x, value='Y', rchoice='&'),
            RulePremise(variable=z, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=y, value='Y', rchoice='&'),
            RulePremise(variable=z, value='Y', rchoice=')')
        ]
        root2 = self.parser.parse(plist2)

        self.assertTrue(treecmp(root1, root2))

    def test_bigone(self):

        # (a|b)&(c|d)&(e|f)
        a = Variable(id=100,name='a')
        b = Variable(id=101,name='b')
        c = Variable(id=102,name='c')
        d = Variable(id=103,name='d')
        e = Variable(id=104,name='e')
        f = Variable(id=105,name='f')

        plist1 = [
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='|'),
            RulePremise(variable=b, value='Y', rchoice=') &'),
            RulePremise(lchoice='(', variable=c, value='Y', rchoice='|'),
            RulePremise(variable=d, value='Y', rchoice=') &'),
            RulePremise(lchoice='(', variable=e, value='Y', rchoice='|'),
            RulePremise(variable=f, value='Y', rchoice=')')
        ]
        root1 = self.parser.parse(plist1)
        root1 = wff_dnf(root1)

        # a&c&e|b&c&e|a&d&e|b&d&e|a&c&f|b&c&f|a&d&f|b&d&f
        plist2 = [
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=c, value='Y', rchoice=' &'),
            RulePremise(variable=e, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=b, value='Y', rchoice='&'),
            RulePremise(variable=c, value='Y', rchoice=' &'),
            RulePremise(variable=e, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=d, value='Y', rchoice=' &'),
            RulePremise(variable=e, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=b, value='Y', rchoice='&'),
            RulePremise(variable=d, value='Y', rchoice=' &'),
            RulePremise(variable=e, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=c, value='Y', rchoice=' &'),
            RulePremise(variable=f, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=b, value='Y', rchoice='&'),
            RulePremise(variable=c, value='Y', rchoice=' &'),
            RulePremise(variable=f, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=d, value='Y', rchoice=' &'),
            RulePremise(variable=f, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=b, value='Y', rchoice='&'),
            RulePremise(variable=d, value='Y', rchoice=' &'),
            RulePremise(variable=f, value='Y', rchoice=')')
        ] 
        root2 = self.parser.parse(plist2)

        self.assertTrue(treecmp(root1, root2))

    def test_bigtwo(self):
        #"A & (B & (C | D) | E) => (A & B & C) | (A & B & D) | (A & E)"
        a = Variable(id=100,name='a')
        b = Variable(id=101,name='b')
        c = Variable(id=102,name='c')
        d = Variable(id=103,name='d')
        e = Variable(id=104,name='e')

        plist1 = [
            RulePremise(variable=a, value='Y', rchoice=' & ('),
            RulePremise(variable=b, value='Y', rchoice=' & ('),
            RulePremise(variable=c, value='Y', rchoice='|'),
            RulePremise(variable=d, value='Y', rchoice=') |'),
            RulePremise(variable=e, value='Y', rchoice=')'),
        ]
        root1 = self.parser.parse(plist1)
        root1 = wff_dnf(root1)

        plist2 = [
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=b, value='Y', rchoice=' &'),
            RulePremise(variable=c, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=b, value='Y', rchoice=' &'),
            RulePremise(variable=d, value='Y', rchoice=') |'),
            RulePremise(lchoice='(', variable=a, value='Y', rchoice='&'),
            RulePremise(variable=e, value='Y', rchoice=')')
        ]
        root2 = self.parser.parse(plist2)
        self.assertTrue(treecmp(root1, root2))

isvar = lambda node,nid,value:True if node.ptype == PTYPE_VAR and node.left == nid and node.right == value else False

class FlattenNodeTests(TestCase):

    def setUp(self):
        self.parser = PremiseParser()

    def test_empty(self):
        # none
        node_list = []
        flatten_node(None, node_list)
        self.assertTrue(len(node_list) == 0)

    def test_var_simple(self):
        # none
        node_list = []
        node = PremiseNode(PTYPE_VAR, 100, 'Y')
        flatten_node(node, node_list)
        self.assertTrue(len(node_list) == 1)
        self.assertTrue(node_list[0] == node)

    def test_and_simple(self):
        # none
        node_list = []
        lnode = PremiseNode(PTYPE_VAR, 100, 'Y')
        rnode = PremiseNode(PTYPE_VAR, 101, 'Y')
        node = PremiseNode(PTYPE_AND, lnode, rnode)
        flatten_node(node, node_list)
        self.assertTrue(len(node_list) == 2)
        self.assertTrue(node_list[0] == lnode)
        self.assertTrue(node_list[1] == rnode)

    def test_or_simple(self):
        node_list = []
        lnode = PremiseNode(PTYPE_VAR, 100, 'Y')
        rnode = PremiseNode(PTYPE_VAR, 101, 'Y')
        node = PremiseNode(PTYPE_OR, lnode, rnode)
        flatten_node(node, node_list)
        self.assertTrue(len(node_list) == 2)
        self.assertTrue(node_list[0] == lnode)
        self.assertTrue(node_list[1] == rnode)

    def test_and_chain(self):
        a = Variable(id=100,name='a')
        b = Variable(id=101,name='b')
        c = Variable(id=102,name='c')
        d = Variable(id=103,name='d')
        e = Variable(id=104,name='e')
        f = Variable(id=105,name='f')
        plist = [
            RulePremise(variable=a, value='Y', rchoice='&'),
            RulePremise(variable=b, value='N', rchoice='&'),
            RulePremise(variable=c, value='Y', rchoice='&'),
            RulePremise(variable=d, value='N', rchoice='&'),
            RulePremise(variable=e, value='Y', rchoice='&'),
            RulePremise(variable=f, value='N')
        ]
        root = self.parser.parse(plist)
        node_list = []
        flatten_node(root, node_list)
        self.assertTrue(len(node_list) == 6)
        self.assertTrue(isvar(node_list[0], a.id, 'Y'))
        self.assertTrue(isvar(node_list[1], b.id, 'N'))
        self.assertTrue(isvar(node_list[2], c.id, 'Y'))
        self.assertTrue(isvar(node_list[3], d.id, 'N'))
        self.assertTrue(isvar(node_list[4], e.id, 'Y'))
        self.assertTrue(isvar(node_list[5], f.id, 'N'))

    def test_or_chain(self):
        a = Variable(id=100,name='a')
        b = Variable(id=101,name='b')
        c = Variable(id=102,name='c')
        d = Variable(id=103,name='d')
        e = Variable(id=104,name='e')
        f = Variable(id=105,name='f')
        plist = [
            RulePremise(variable=a, value='Y', rchoice='|'),
            RulePremise(variable=b, value='N', rchoice='|'),
            RulePremise(variable=c, value='Y', rchoice='|'),
            RulePremise(variable=d, value='N', rchoice='|'),
            RulePremise(variable=e, value='Y', rchoice='|'),
            RulePremise(variable=f, value='N')
        ]
        root = self.parser.parse(plist)
        node_list = []
        flatten_node(root, node_list)
        self.assertTrue(len(node_list) == 6)
        self.assertTrue(isvar(node_list[0], a.id, 'Y'))
        self.assertTrue(isvar(node_list[1], b.id, 'N'))
        self.assertTrue(isvar(node_list[2], c.id, 'Y'))
        self.assertTrue(isvar(node_list[3], d.id, 'N'))
        self.assertTrue(isvar(node_list[4], e.id, 'Y'))
        self.assertTrue(isvar(node_list[5], f.id, 'N'))

class EngineTests(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.v1 = Variable.objects.create(name='v1', ask=False)
        self.v2 = Variable.objects.create(name='v2', ask=False)
        self.v3 = Variable.objects.create(name='v3', ask=False)
        self.v4 = Variable.objects.create(name='v4', ask=False)

        self.rs_simple = RuleSet.objects.create(name='rs-simple')
        rule1 = self.rs_simple.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value='Y')
        rule1.ruleconclusion_set.create(variable=self.v2, value='Y')

        self.rs_and = RuleSet.objects.create(name='rs-and')
        rule1 = self.rs_and.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value='Y',rchoice='&')
        rule1.rulepremise_set.create(variable=self.v2, value='Y')
        rule1.ruleconclusion_set.create(variable=self.v3, value='Y')

        self.rs_or = RuleSet.objects.create(name='rs-or')
        rule1 = self.rs_or.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value='Y')
        rule1.ruleconclusion_set.create(variable=self.v3, value='Y')
        rule2 = self.rs_or.rule_set.create()
        rule2.rulepremise_set.create(variable=self.v2, value='Y')
        rule2.ruleconclusion_set.create(variable=self.v3, value='Y')

        self.rs_infer = RuleSet.objects.create(name='rs-infer')
        rule1 = self.rs_infer.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value='Y')
        rule1.ruleconclusion_set.create(variable=self.v2, value='Y')

        rule2 = self.rs_infer.rule_set.create()
        rule2.rulepremise_set.create(variable=self.v2, value='Y')
        rule2.ruleconclusion_set.create(variable=self.v3, value='Y')

        rule3 = self.rs_infer.rule_set.create()
        rule3.rulepremise_set.create(variable=self.v3, value='Y')
        rule3.ruleconclusion_set.create(variable=self.v4, value='Y')

    def test_empty(self):
        empty_list = []
        state = Engine(empty_list)
        self.assertEquals(state.get_rulesets(), empty_list)
        self.assertEquals(state.get_vars(), empty_list)
        self.assertEquals(state.get_tests(), empty_list)
        self.assertEquals(state.get_recommends(), empty_list)
        
    def test_simple(self):
        rulesets = [ self.rs_simple.id ]
        answers = [ (self.v1.id, 'Y') ]
        nvars = list(answers)
        nvars.append((self.v2.id, 'Y'))
        tests = []
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), tests)

    def test_and_tt(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, 'Y'), (self.v2.id, 'Y') ]
        nvars = list(answers)
        nvars.append((self.v3.id, 'Y')) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_and_tf(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, 'Y'), (self.v2.id, 'N') ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_and_ft(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, 'N'), (self.v2.id, 'Y') ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_and_ff(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, 'N'), (self.v2.id, 'N') ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_tt(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, 'Y'), (self.v2.id, 'Y') ]
        nvars = list(answers)
        nvars.append((self.v3.id, 'Y')) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_tf(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, 'Y'), (self.v2.id, 'N') ]
        nvars = list(answers)
        nvars.append((self.v3.id,'Y')) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_ft(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, 'N'), (self.v2.id, 'Y') ]
        nvars = list(answers)
        nvars.append((self.v3.id,'Y')) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_ff(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, 'N'), (self.v2.id, 'N') ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_inference(self):
        rulesets = [ self.rs_infer.id ]
        answers = [ (self.v1.id, 'Y') ]
        nvars = [ (self.v1.id, 'Y'), 
                  (self.v2.id, 'Y'),
                  (self.v3.id, 'Y'), 
                  (self.v4.id, 'Y') 
                ]
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)


class ViewTests(TestCase):

    def setUp(self):
        self.v1 = Variable.objects.create(name='v1', ask=False)
        self.v2 = Variable.objects.create(name='v2', ask=False)

        self.rs_view = RuleSet.objects.create(name='rs_view')
        rule1 = self.rs_view.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value='Y')
        rule1.ruleconclusion_set.create(variable=self.v2, value='Y')

        self.profile1 = Profile.objects.create(name='profile1', ruleset=self.rs_view)
        self.user1 = User.objects.create_user('user1','user1@aha.com','user1')
        account = self.user1.get_profile()
        account.profile = self.profile1
        account.save()

    def test_get_ids(self):
        slist = [ id for id in xrange(10) ]
        tlist = [TestModel(id) for id in slist]
        elist = get_ids(tlist)
        self.assertEqual(slist, elist)

    def test_get_answers(self):
        slist =  [ (num, 'Y' if (num % 2) else 'N') for num in xrange(10) ] 
        tlist = [ ( 'answer_%d' % num, 'y' if value=='Y' else 'n')  for num,value in slist ]
        elist = get_answers(tlist)
        self.assertEquals(slist, elist)

    def test_start_state(self):
        # check initial facts with no requires are selected
        test_ids = []
        state = start_state(self.user1)
        self.assertEquals(state.get_tests(), test_ids)

    def test_next_state(self):
        # check pass facts are returned when given appropriate answers
        state = start_state(self.user1)
        answers = [ (self.v1.id, 'Y') ]
        nvars = [ (self.v1.id, 'Y'), 
                  (self.v2.id, 'Y')]
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        
    #Custom filter tests
class TemplateTests(TestCase):

    def setUp(self):
        self.testString = "A quick brown fox jumps over the lazy dog"
        
    def test_isImg(self):
        imgLink1 = "www.foo.com/test1.JPG"
        imgLink2 = "www.foo.com/test1.Jpeg"
        imgLink3 = "www.foo.com/test1.gif"
        imgLink4 = "www.foo.com/test1.svg"
        imgLink5 = "www.foo.com/test1.png"
        nonImgLink = "www.bar.com/foo.exe"
        self.assertEquals(isImg(imgLink1),True)
        self.assertEquals(isImg(imgLink2),True)
        self.assertEquals(isImg(imgLink3),True)
        self.assertEquals(isImg(imgLink4),True)
        self.assertEquals(isImg(imgLink5),True)
        self.assertEquals(isImg(nonImgLink),False)
        
    def test_contains(self):
        subString = "quick brown"
        nonSubString = "slow red"
        self.assertEquals(contains(self.testString,subString),True)
        self.assertEquals(contains(self.testString,nonSubString),False)
    
    def test_lslice(self):
        test = lslice(self.testString,"5")
        self.assertEquals(test,self.testString[5:])
        
    def test_escapeJS(self):
        test = "f o\"o'b(a)r<i>u[s]"
        self.assertEquals(escapeForJS(test),"foobarius")
