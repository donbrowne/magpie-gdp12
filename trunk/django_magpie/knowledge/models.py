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

def get_answers(items):
    answers = []
    for name,value in items:
        if name.startswith('answer_'):
            qid = int(name[len('answer_'):])
            istrue = value == 'y'
            answers.append((qid, istrue))
    return answers

# update recommends + calculate next set of questions
def next_sess(rule_ids, answers, rec_ids):
    # build list of rules that match all answers
    rules = []
    questions = []
    recommends = list(Recommend.objects.filter(id__in=rec_ids))
    for rule in Rule.objects.filter(id__in=rule_ids):
        # check if expected answers match those given
        match_all = True
        for ranswer in rule.ruleanswer_set.all():
            expect = (ranswer.question.id, ranswer.answer)
            if expect not in answers:
                match_all = False
                break
        if match_all:
            for recommend in rule.recommends.all():
                if recommend not in recommends:
                    recommends.append(recommend)
            for child_rule in rule.rule_set.all():
                if child_rule not in rules:
                    rules.append(child_rule)
                for ranswer in child_rule.ruleanswer_set.all():
                    if ranswer.question not in questions:
                        questions.append(ranswer.question)
    return rules, questions, recommends

# start a q+a session
def start_sess():
    rules = []
    questions = []
    recommends = []
    for rule in Rule.objects.filter(requires__isnull=True):
        if rule not in rules:
            rules.append(rule)
        for ranswer in rule.ruleanswer_set.all():
            if ranswer.question not in questions:
                questions.append(ranswer.question)
    return rules, questions

