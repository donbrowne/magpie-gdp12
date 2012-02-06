from django.db import models

# Create your models here.
class Fact(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=255)
    yes_fact = models.ForeignKey(Fact, related_name='yes_fact')
    no_fact = models.ForeignKey(Fact, related_name='no_fact')
    def __unicode__(self):
        return self.text

class Recommendation(models.Model):
    text = models.CharField(max_length=255)
    def __unicode__(self):
        return self.text

class Rule(models.Model):
    facts = models.ManyToManyField(Fact)
    recommendations = models.ManyToManyField(Recommendation)
    def __unicode__(self):
        return str(self.id)
