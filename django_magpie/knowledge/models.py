from django.db import models
import django.contrib.auth.models

class Question(models.Model):
    text = models.CharField(max_length=255)
    def __unicode__(self):
        return self.text
        
class ResourceFile(models.Model):
    description = models.CharField(max_length=255)
#Upload to the media root directory 
#(upload_to is the subdir of the media root directory
#TODO: Replace . with user name
    file  = models.FileField(upload_to=".")
    group = models.ManyToManyField(django.contrib.auth.models.Group,blank=True,null=True)
    def __unicode__(self):
        return self.description    

class Recommend(models.Model):
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
        
class UnansweredReason(object): 
    def __init__(self, recs, question):
        self.question = question
        self.recs = recs
        
class RecsSummary(object): 
    def __init__(self, text, details, pmlPath, vidLink):
        self.text = text
        self.links = details
        self.pmlPath = pmlPath
        self.vidLink = vidLink
        
def compareGroups(userGroup, fileGroup):
    if not fileGroup: 
        return True
    else:
        return bool(list(set(userGroup) & set(fileGroup)))
        
def compareGroupUrl(url,userGroup):
   rFile = None
   for files in ResourceFile.objects.all():
       print url
       print "HELLO"
       print files.file.url
       if files.file.url == url:
           rFile = files
           break
   if not rFile:
       return False
   else:
       return compareGroups(userGroup, rFile.group.all())
        
#Pack together the recommendation data in a nice way.        
def recSummaryClosure(userGroup):
    def getRecSummary(rec):
        recsList = []
        pmlPath = None
        vidLink = None
        if rec.videoLink != None and compareGroups(userGroup,rec.videoLink.group.all()):
            vidLink = rec.videoLink.file.url
            print vidLink
        if rec.pmlLink != None and compareGroups(userGroup,rec.pmlLink.group.all()):
            recsList.append(("PML Link", rec.pmlLink.file.url))
            pmlPath = rec.pmlLink.file.name
        for others in rec.otherLinks.all():
            if compareGroups(userGroup,others.group.all()):
                recsList.append((others.description,others.file.url))
        for link in ExternalLink.objects.filter(rec=rec.id):
            print link
            recsList.append((link.description,link.link))
        return RecsSummary(rec.text,recsList,pmlPath,vidLink)
    return getRecSummary

class FactState(object):
    def __init__(self, test_ids, pass_ids=None, answers=None, falseFactIDs=None, notAnswered=None):
        # default arguments beware
        if pass_ids is None: 
            pass_ids = []
        if answers is None:
            answers = []
        if falseFactIDs is None:
            falseFactIDs = []
        if notAnswered is None:
            notAnswered=[]
        self.test_ids = test_ids
        self.pass_ids = pass_ids
        self.falseFactIDs = falseFactIDs
        self.notAnswered = notAnswered
        self.answers = answers

    def get_answers(self):
        return self.answers

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
        
    def getUnansweredReasons(self):
        id_set = set()
        reasons = []
        for pair in self.notAnswered:
            fact = Fact.objects.get(id=pair[0])
            recommends = []
            for recommend in fact.recommends.all():
                if recommend.id not in id_set:
                    id_set.add(recommend.id)
                    recommends.append(recommend.text)
            question = Question.objects.get(id=pair[1])
            reasons.append(UnansweredReason(recommends,question))
        return reasons

    # given some answers calculate next set of facts to test
    def next_state(self, answers):
        test_ids = []
        pass_ids = self.pass_ids
        falseFactIDs = self.falseFactIDs
        notAnswered = self.notAnswered
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
                if qid not in ans_dict:
                    match_all = False
                    if (qid,fact.id) not in notAnswered:
                        notAnswered.append((fact.id,qid))
                    break
                elif ans_dict[qid] != fquestion.answer:
                    match_all = False
                    if (qid,fact.id) in notAnswered:
                        notAnswered.remove((fact.id,qid))
                    falseFactIDs.append(fact.id)
                    break
                elif (qid,fact.id) in notAnswered:
                        notAnswered.remove((fact.id,qid))
            if match_all:
                pass_ids.append(fact.id)
                for child_fact in fact.fact_set.all():
                    if child_fact.id not in test_ids:
                        test_ids.append(child_fact.id)
        return FactState(test_ids, pass_ids, ans_dict.items(), falseFactIDs, notAnswered)

# Factory start a q+a session
def start_state(user):
    test_ids = []
    if user.is_anonymous():
        user_types = []	
    else:
        profile= user.get_profile()
        user_types = profile.types.all()
    for fact in Fact.objects.filter(requires__isnull=True):
        num_utypes = 0 
        user_fact = False
        for utype in fact.usertype_set.all():
            num_utypes = num_utypes + 1
            if utype in user_types:
                user_fact = True
                break
        if (user_fact or num_utypes == 0) and fact.id not in test_ids:
            if len(fact.factquestion_set.all()) == 0:
                ids = get_ids(fact.fact_set.all())
                test_ids.extend(ids)
            else:
                test_ids.append(fact.id)
    return FactState(test_ids)
