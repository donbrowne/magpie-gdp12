from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    def __unicode__(self):
        return self.text

class Recommend(models.Model):
    text = models.CharField(max_length=255)
    def __unicode__(self):
        return self.text

class Rule(models.Model):
    name = models.CharField(max_length=30)
    requires = models.ManyToManyField('Rule',blank=True)
    recommends = models.ManyToManyField(Recommend,blank=True)
    def __unicode__(self):
        return self.name

#BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class RuleAnswer(models.Model):
    parent = models.ForeignKey(Rule)
    question = models.ForeignKey(Question)
    answer = models.BooleanField()
    def __unicode__(self):
        return self.question.text + ' ' + str(self.answer)

# TODO make a helper class
def get_ids(alist):
    return map(lambda elem:elem.id, alist)

# TODO should this be in views
def get_answers(items):
    answers = []
    for name,value in items:
        if name.startswith('answer_'):
            qid = int(name[len('answer_'):])
            istrue = value == 'y'
            answers.append((qid, istrue))
    return answers

class FactState(object):
    def __init__(self, test_ids, pass_ids=[], answers=[]):
        self.test_ids = test_ids
        self.pass_ids = pass_ids
        self.answers = answers

    # return list of questions for rule set not yet answered
    def get_questions(self):
        questions = []
        ans_dict = dict(self.answers)
        for rule in Rule.objects.filter(id__in=self.test_ids):
            for ranswer in rule.ruleanswer_set.all():
                question = ranswer.question
                if question.id not in ans_dict and question not in questions:
                    questions.append(question)
        return questions

    # return list of recommendation for rule set answered
    def get_recommends(self):
        recommends = []
        for rule in Rule.objects.filter(id__in=self.pass_ids):
            for recommend in rule.recommends.all():
                if recommend not in recommends:
                    recommends.append(recommend)
        return recommends

    # given some answers calculate next set of rules to test
    def next_state(self, answers):
        test_ids = []
        pass_ids = self.pass_ids
        # answers = prev + new
        ans_dict = dict(self.answers)
        for item in answers:
            ans_dict[item[0]] = item[1]
        # build list of rules that match all answers
        for rule in Rule.objects.filter(id__in=self.test_ids):
            # check if expected answers match those given
            match_all = True
            for ranswer in rule.ruleanswer_set.all():
                qid = ranswer.question.id
                if qid not in ans_dict or ans_dict[qid] != ranswer.answer:
                    match_all = False
                    break
            if match_all:
                pass_ids.append(rule.id)
                for child_rule in rule.rule_set.all():
                    if child_rule.id not in test_ids:
                        test_ids.append(child_rule.id)
        return FactState(test_ids, pass_ids, ans_dict.items())


# Factory start a q+a session
def start_state():
    test_ids = []
    for rule in Rule.objects.filter(requires__isnull=True):
        if rule.id not in test_ids:
            test_ids.append(rule.id)
    return FactState(test_ids)



