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

