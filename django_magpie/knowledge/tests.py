"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from knowledge.models import Question,Recommend,Fact,get_ids, get_answers,start_state

# dummy class used for tests
class TestModel:
    def __init__(self, id):
        self.id = id

class KnowledgeTests(TestCase):

    def setUp(self):
        self.f1 = Fact.objects.create(name='one')
        self.q1 = Question.objects.create(text='Do you like music')
        self.f1.factquestion_set.create(question=self.q1, answer=True)
        self.r1 = Recommend.objects.create(text='Try amazon.com')
        self.f1.recommends.add(self.r1)
        
        self.f2 = Fact.objects.create(name='two')
        self.q2 = Question.objects.create(text='Do you like fish')
        self.f2.factquestion_set.create(question=self.q2, answer=True)
        self.q3 = Question.objects.create(text='Do you like jazz')
        self.f2.factquestion_set.create(question=self.q3, answer=True)
        self.r2 = Recommend.objects.create(text='Try sushi-bluz resturatant')
        self.f2.recommends.add(self.r2)
        

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
        test_ids = [ self.f1.id, self.f2.id ]
        state = start_state()
        self.assertEquals(state.test_ids, test_ids)

    def test_next_state(self):
        # check pass facts are returned when given appropriate answers
        state = start_state()
        answers = [ (self.q2.id, True), (self.q3.id, True) ]
        nstate = state.next_state(answers)
        pass_ids = [ self.f2.id ] 
        self.assertEquals(state.pass_ids, pass_ids)
