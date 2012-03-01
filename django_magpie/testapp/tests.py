"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from views import get_answers
from django.contrib.auth.models import User

# dummy class used for tests
class TestModel:
    def __init__(self, id):
        self.id = id
        
class EngineTests(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.v1 = Variable.objects.create(name='v1', ask=False)
        self.v2 = Variable.objects.create(name='v2', ask=False)
        self.v3 = Variable.objects.create(name='v3', ask=False)
        self.v4 = Variable.objects.create(name='v4', ask=False)

        self.rs_simple = RuleSet.objects.create(name='rs-simple')
        rule1 = self.rs_simple.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value=True)
        rule1.ruleconclusion_set.create(variable=self.v2, value=True)

        self.rs_and = RuleSet.objects.create(name='rs-and')
        rule1 = self.rs_and.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value=True)
        rule1.rulepremise_set.create(variable=self.v2, value=True)
        rule1.ruleconclusion_set.create(variable=self.v3, value=True)

        self.rs_or = RuleSet.objects.create(name='rs-or')
        rule1 = self.rs_or.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value=True)
        rule1.ruleconclusion_set.create(variable=self.v3, value=True)
        rule2 = self.rs_or.rule_set.create()
        rule2.rulepremise_set.create(variable=self.v2, value=True)
        rule2.ruleconclusion_set.create(variable=self.v3, value=True)

        self.rs_infer = RuleSet.objects.create(name='rs-infer')
        rule1 = self.rs_infer.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value=True)
        rule1.ruleconclusion_set.create(variable=self.v2, value=True)

        rule2 = self.rs_infer.rule_set.create()
        rule2.rulepremise_set.create(variable=self.v2, value=True)
        rule2.ruleconclusion_set.create(variable=self.v3, value=True)

        rule3 = self.rs_infer.rule_set.create()
        rule3.rulepremise_set.create(variable=self.v3, value=True)
        rule3.ruleconclusion_set.create(variable=self.v4, value=True)

    def test_empty(self):
        empty_list = []
        state = Engine(empty_list)
        self.assertEquals(state.get_rulesets(), empty_list)
        self.assertEquals(state.get_vars(), empty_list)
        self.assertEquals(state.get_tests(), empty_list)
        self.assertEquals(state.get_recommends(), empty_list)
        
    def test_simple(self):
        rulesets = [ self.rs_simple.id ]
        answers = [ (self.v1.id, True), (self.v2.id, True) ]
        tests = []
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), answers)
        self.assertEquals(state.get_tests(), tests)

    def test_and_tt(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, True), (self.v2.id, True) ]
        nvars = list(answers)
        nvars.append((self.v3.id,True)) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_and_tf(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, True), (self.v2.id, False) ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_and_ft(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, False), (self.v2.id, True) ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_and_ff(self):
        rulesets = [ self.rs_and.id ]
        answers = [ (self.v1.id, False), (self.v2.id, False) ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_tt(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, True), (self.v2.id, True) ]
        nvars = list(answers)
        nvars.append((self.v3.id,True)) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_tf(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, True), (self.v2.id, False) ]
        nvars = list(answers)
        nvars.append((self.v3.id,True)) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_ft(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, False), (self.v2.id, True) ]
        nvars = list(answers)
        nvars.append((self.v3.id,True)) 
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_or_ff(self):
        rulesets = [ self.rs_or.id ]
        answers = [ (self.v1.id, False), (self.v2.id, False) ]
        nvars = list(answers)
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)
        self.assertEquals(state.get_tests(), [])

    def test_inference(self):
        rulesets = [ self.rs_infer.id ]
        answers = [ (self.v1.id, True) ]
        nvars = [ (self.v1.id, True), 
                  (self.v2.id, True),
                  (self.v3.id, True), 
                  (self.v4.id, True) 
                ]
        state = Engine(rulesets)
        state.next_state(answers)
        self.assertEquals(state.get_vars(), nvars)


class ViewTests(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.v1 = Variable.objects.create(name='v1', ask=False)
        self.v2 = Variable.objects.create(name='v2', ask=False)

        self.rs_view = RuleSet.objects.create(name='rs_view')
        rule1 = self.rs_view.rule_set.create()
        rule1.rulepremise_set.create(variable=self.v1, value=True)
        rule1.ruleconclusion_set.create(variable=self.v2, value=True)

    def test_get_ids(self):
        slist = [ id for id in xrange(10) ]
        tlist = [TestModel(id) for id in slist]
        elist = get_ids(tlist)
        self.assertEqual(slist, elist)

    def test_get_answers(self):
        slist =  [ (num, True if (num % 2) else False) for num in xrange(10) ] 
        tlist = [ ( 'answer_%d' % num, 'y' if value else 'n')  for num,value in slist ]
        elist = get_answers(tlist)
        self.assertEquals(slist, elist)

    def test_start_state(self):
        # check initial facts with no requires are selected
        test_ids = []
        state = start_state(self.u1)
        self.assertEquals(state.get_tests(), test_ids)

    def test_next_state(self):
        # check pass facts are returned when given appropriate answers
        state = start_state(self.u1)
        answers = [ (self.v1.id, True), (self.v2.id, True) ]
        state.next_state(answers)
        self.assertEquals(state.get_vars(), answers)

