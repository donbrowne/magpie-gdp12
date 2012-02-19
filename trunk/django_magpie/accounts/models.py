from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from knowledge.models import Fact,Question

"""
class UserType(models.Model):
    name = models.CharField(max_length=30)
    facts = models.ManyToManyField('Fact',blank=True)
"""

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    facts = models.ManyToManyField(Fact,blank=True)
    def __unicode__(self):
        return self.user.username

class UserAnswer(models.Model):
    user = models.ForeignKey(UserProfile)
    question = models.ForeignKey(Question)
    answer = models.BooleanField()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# tell us if a new user created
post_save.connect(create_user_profile, sender=User)
