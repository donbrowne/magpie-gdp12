from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from knowledge.models import Fact,Question,get_ids

"""
class UserType(models.Model):
    name = models.CharField(max_length=30)
    facts = models.ManyToManyField('Fact',blank=True)
"""

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    facts = models.ManyToManyField(Fact,blank=True)

    def get_answers(self):
        answers = []
        for uanswer in self.useranswer_set.all():
            answers.append((uanswer.question_id, uanswer.answer))
        return answers

    def save_answers(self, answers):
        ans_dict = dict(answers)
        keys = ans_dict.keys()
        # first update existing answers
        for uanswer in self.useranswer_set.filter(id__in=keys):
            uanswer.answer = ans_dict[uanswer.question_id]
            uanswer.save()
            del ans_dict[uanswer.question_id]
        # now add new ones
        for key,value in ans_dict.items():
            self.useranswer_set.create(question_id=key, answer=value)

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
