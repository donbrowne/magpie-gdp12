from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from knowledge.models import RuleSet,Variable

# Note
# In django user profile is normaly used to mean
# an extended user config but the project has claimed
# the term to mean user types. 
# So to save further confusion we are going to take it
# to mean user types.

class Profile(models.Model):
    name = models.SlugField(max_length=30, unique=True)
    ruleset = models.ForeignKey(RuleSet)

    def __unicode__(self):
        return self.name

# assert some facts before using a ruleset
class ProfileAnswer(models.Model):
    parent = models.ForeignKey(Profile, editable=False)
    variable = models.ForeignKey(Variable)
    value = models.BooleanField()

class Account(models.Model):
    user = models.OneToOneField(User)
    profile = models.ForeignKey(Profile, null=True)

    def get_answers(self):
        answers = []
        for answer in self.accountanswer_set.all():
            answers.append((answer.variable_id, answer.value))
        return answers

    def save_answers(self, answers):
        ans_dict = dict(answers)
        keys = ans_dict.keys()
        # first update existing answers
        for uanswer in self.accountanswer_set.filter(id__in=keys):
            uanswer.value = ans_dict[uanswer.variable_id]
            uanswer.save()
            del ans_dict[uanswer.variable_id]
        # now add new ones
        for key,value in ans_dict.items():
            self.accountanswer_set.create(variable_id=key, value=value)

    def __unicode__(self):
        return self.user.username

# We store a users answers here
class AccountAnswer(models.Model):
    parent = models.ForeignKey(Account, editable=False)
    variable = models.ForeignKey(Variable)
    value = models.BooleanField()

def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

# tell us if a new auth user created
post_save.connect(create_account, sender=User)

# django snippet 1875
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')

def create_testuser(app, created_models, verbosity, **kwargs):
  if not settings.DEBUG:
    return

  try:
    dbconfig = settings.DATABASES['default']
    user = dbconfig['USER']
    password = dbconfig['PASSWORD']
  except KeyError:
    print 'Invalid settings.py'
    return

  try:
    auth_models.User.objects.get(username=user)
  except auth_models.User.DoesNotExist:
    print '*' * 80
    print 'Creating test user -- login: %s, password: %s' %( user, password)
    print '*' * 80
    assert auth_models.User.objects.create_superuser(user, 'x@x.com', password)
  else:
    print 'Admin user already exists.'

signals.post_syncdb.connect(create_testuser,
    sender=auth_models, dispatch_uid='common.models.create_testuser')


