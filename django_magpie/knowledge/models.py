from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    def __unicode__(self):
        return self.text

class Recommend(models.Model):
    text = models.CharField(max_length=255)
    def __unicode__(self):
        return self.text

class Fact(models.Model):
    name = models.CharField(max_length=30)
    requires = models.ManyToManyField('Fact',blank=True)
    recommends = models.ManyToManyField(Recommend,blank=True)
    def __unicode__(self):
        return self.name

#BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class FactQuestion(models.Model):
    fact = models.ForeignKey(Fact)
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

class Reason(object):
    def __init__(self, text, qa_list):
        self.text = text
        self.qa_list = qa_list

class FactState(object):
    def __init__(self, test_ids, pass_ids=[], answers=[], falseFactIDs=[]):
        self.test_ids = test_ids
        self.pass_ids = pass_ids
        self.falseFactIDs = falseFactIDs
        self.answers = answers

    # return list of questions for fact set not yet answered
    def get_questions(self):
        questions = []
        ans_dict = dict(self.answers)
        for fact in Fact.objects.filter(id__in=self.test_ids):
            for fquestion in fact.factquestion_set.all():
                question = fquestion.question
                if question.id not in ans_dict and question not in questions:
                    questions.append(question)
        return questions

    # return list of recommendation for fact set answered
    def get_recommends(self):
        recommends = []
        for fact in Fact.objects.filter(id__in=self.pass_ids):
            for recommend in fact.recommends.all():
                if recommend not in recommends:
                    recommends.append(recommend)
        return recommends
    
    #Return list of recommendations that have been ruled out
    def getNonRecommended(self):
        non_recommended = []
        for fact in Fact.objects.filter(id__in=self.falseFactIDs):
            for nr in fact.recommends.all():
                if nr not in non_recommended:
                    non_recommended.append(nr)
        return non_recommended
        
    #Get a list of recommendations that are not applicable yet
    def getOtherRecs(self):
        other_recommended = []
        for fact in Fact.objects.exclude(id__in=self.pass_ids).exclude(id__in=self.falseFactIDs):
            for other in fact.recommends.all():
                if other not in other_recommended:
                    other_recommended.append(other)
        return other_recommended

    def get_reasons(self):
        reasons = []
        ans_dict = dict(self.answers)
        id_set = set()
        for fact in Fact.objects.filter(id__in=self.pass_ids):
            # first get unique list of recommends
            recommends = []
            for recommend in fact.recommends.all():
                if recommend.id not in id_set:
                    id_set.add(recommend.id)
                    recommends.append(recommend)
            # now build questions+answer list
            qa_list = []
            for fquestion in fact.factquestion_set.all():
                question = fquestion.question
                #'%s ? %s' % (question.text, 'Yes'
                qa_list.append((question.text, ans_dict[question.id]))
            # generate reason for each recommend
            for recommend in recommends:
                reasons.append(Reason(recommend.text, qa_list))
        return reasons
        
    def getNonReasons(self):
        reasons = []
        ans_dict = dict(self.answers)
        id_set = set()
        for fact in Fact.objects.filter(id__in=self.falseFactIDs):
            # first get unique list of recommends
            recommends = []
            for recommend in fact.recommends.all():
                if recommend.id not in id_set:
                    id_set.add(recommend.id)
                    recommends.append(recommend)
            # now build questions+answer list
            qa_list = []
            for fquestion in fact.factquestion_set.all():
                question = fquestion.question
                #'%s ? %s' % (question.text, 'Yes'
                qa_list.append((question.text, ans_dict[question.id]))
            # generate reason for each recommend
            for recommend in recommends:
                reasons.append(Reason(recommend.text, qa_list))
        return reasons

    # given some answers calculate next set of facts to test
    def next_state(self, answers):
        test_ids = []
        pass_ids = self.pass_ids
        falseFactIDs = self.falseFactIDs
        # answers = prev + new
        ans_dict = dict(self.answers)
        for item in answers:
            ans_dict[item[0]] = item[1]
        # build list of facts that match all answers
        for fact in Fact.objects.filter(id__in=self.test_ids):
            # check if expected answers match those given
            match_all = True
            for fquestion in fact.factquestion_set.all():
                qid = fquestion.question.id
                if ans_dict[qid] != fquestion.answer:
                    match_all = False
                    falseFactIDs.append(fact.id)
                    break
                elif qid not in ans_dict:
                    match_all = False
                    break
            if match_all:
                pass_ids.append(fact.id)
                for child_fact in fact.fact_set.all():
                    if child_fact.id not in test_ids:
                        test_ids.append(child_fact.id)
        return FactState(test_ids, pass_ids, ans_dict.items(), falseFactIDs)


# Factory start a q+a session
def start_state():
    test_ids = []
    for fact in Fact.objects.filter(requires__isnull=True):
        if fact.id not in test_ids:
            test_ids.append(fact.id)
    return FactState(test_ids)



