"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from knowledge.models import get_ids, get_answers

# dummy class used for tests
class TestModel:
    def __init__(self, id):
        self.id = id

class KnowledgeTests(TestCase):

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
        
