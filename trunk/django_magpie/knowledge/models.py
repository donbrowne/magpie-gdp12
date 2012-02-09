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

class FactAnswer(models.Model):
    parent = models.ForeignKey(Fact)
    question = models.ForeignKey(Question)
    answer = models.BooleanField()
    def __unicode__(self):
        return self.question.text + ' ' + str(self.answer)

