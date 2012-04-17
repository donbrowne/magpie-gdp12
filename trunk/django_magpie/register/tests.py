from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import signals
from models import Account,Profile,create_testuser,create_account
from knowledge.models import Variable
from forms import RegistrationForm, AccountForm

import string 
import random

def random_string(length):
    return "".join([random.choice(string.lowercase+string.digits) for x in range(1, length)])

def makeurl(url,redirect):
    return '%s?next=%s' %(reverse(url),redirect)

class RegisterTests(TestCase):

    def setUp(self):
        self.redirect = '/' + random_string(10)
        self.reg_url = makeurl('register',self.redirect)
        self.login_url = makeurl('login',self.redirect)

    def test_register_url(self):
        rsp = self.client.get(self.reg_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.context['next'], self.redirect)
        self.assertTrue(isinstance(rsp.context['form'],RegistrationForm))

    def test_register_new_user(self):
        username = random_string(10)
        password =  User.objects.make_random_password(10)
        email = '%s@test.com' % random_string(10)

        rsp = self.client.post(self.reg_url, {
                'username': username,
                'password1': password,
                'password2': password,
                'email' : email
                })

        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp['Location'], 'http://testserver' + self.redirect)

        user = User.objects.get(username=username)
        self.assertEqual(user.username,username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_authenticated())
        self.assertTrue(isinstance(user.get_profile(),Account))

    def test_login_url(self):
        rsp = self.client.get(self.login_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertTrue(isinstance(rsp.context['form'],AuthenticationForm))

    def test_login_user(self):
        username = random_string(10)
        email = '%s@test.com' % random_string(10)
        password1 =  User.objects.make_random_password(10)
        User.objects.create_user(username,email,password1)

        rsp = self.client.post(self.login_url, 
                            { 'username':username, 
                              'password': password1 })
        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp['Location'], 'http://testserver' + self.redirect)


class AccountTests(TestCase):

    def setUp(self):
        self.redirect = '/' + random_string(10)
        self.account_url = makeurl('account',self.redirect)
        self.user = User.objects.create_user('test','test@test.com','test')
    
    def test_unicode(self):
        account = self.user.get_profile()
        self.assertEquals(self.user.username,str(account))

    def test_account_url(self):
        rsp = self.client.get(self.account_url)
        self.assertEqual(rsp.status_code, 302)

    def test_edit_account(self):
        username = random_string(10)
        email = '%s@test.com' % random_string(10)
        password =  User.objects.make_random_password(10)
        User.objects.create_user(username,email,password)
        self.client.login(username=username,password=password)
        rsp = self.client.get(self.account_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertTrue(isinstance(rsp.context['form'],AccountForm))
        first_name=random_string(10)
        last_name=random_string(10)
        email = '%s@test.com' % username
        rsp = self.client.post(self.account_url, {
                'first_name': first_name,
                'last_name': last_name,
                'email' : email
                })

        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp['Location'], 'http://testserver' + self.redirect)

        user = User.objects.get(username=username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)

    def test_edit_account_werrors(self):
        username = random_string(10)
        email = '%s@test.com' % random_string(10)
        password =  User.objects.make_random_password(10)
        User.objects.create_user(username,email,password)
        self.client.login(username=username,password=password)
        rsp = self.client.get(self.account_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertTrue(isinstance(rsp.context['form'],AccountForm))
        first_name=random_string(10)
        last_name=random_string(10)
        email = 'invalid_email' 
        rsp = self.client.post(self.account_url, {
                'first_name': first_name,
                'last_name': last_name,
                'email' : email
                })
        self.assertEqual(rsp.status_code, 200)

    def test_save_answers_add(self):
        v1 = Variable.objects.create(name='v1', ask=False)
        v2 = Variable.objects.create(name='v2', ask=False)
        v3 = Variable.objects.create(name='v3', ask=False)
        v4 = Variable.objects.create(name='v4', ask=False)
        save_list = [ (v1.id,'Y'), (v2.id,'N'),(v3.id,'Y'),(v4.id,'N')]
        account = self.user.get_profile()
        account.save_answers(save_list)
        get_list = account.get_answers()
        self.assertEqual(save_list, get_list)

    def test_save_answers_update(self):
        v1 = Variable.objects.create(name='v1', ask=False)
        v2 = Variable.objects.create(name='v2', ask=False)
        v3 = Variable.objects.create(name='v3', ask=False)
        v4 = Variable.objects.create(name='v4', ask=False)
        save_list1 = [ (v1.id,'Y'), (v2.id,'Y'),(v3.id,'Y'),(v4.id,'Y')]
        account = self.user.get_profile()
        account.save_answers(save_list1)
        save2_list = [ (v1.id,'N'), (v2.id,'N'),(v3.id,'N'),(v4.id,'N')]
        account.save_answers(save2_list)
        get_list = account.get_answers()
        self.assertEqual(save2_list, get_list)
    
    def test_save_answers_del(self):
        v1 = Variable.objects.create(name='v1', ask=False)
        v2 = Variable.objects.create(name='v2', ask=False)
        v3 = Variable.objects.create(name='v3', ask=False)
        v4 = Variable.objects.create(name='v4', ask=False)
        save1_list = [ (v1.id,'Y'), (v2.id,'Y'),(v3.id,'Y'),(v4.id,'Y')]
        account = self.user.get_profile()
        account.save_answers(save1_list)
        save2_list = [ (v2.id,'N'),(v3.id,'N')]
        account.save_answers(save2_list)
        get_list = account.get_answers()
        self.assertEqual(save2_list, get_list)

    def test_save_answers_add_update_del(self):
        v1 = Variable.objects.create(name='v1', ask=False)
        v2 = Variable.objects.create(name='v2', ask=False)
        v3 = Variable.objects.create(name='v3', ask=False)
        v4 = Variable.objects.create(name='v4', ask=False)
        v5 = Variable.objects.create(name='v5', ask=False)
        v6 = Variable.objects.create(name='v6', ask=False)
        save1_list = [ (v1.id,'Y'), (v2.id,'Y'),(v3.id,'Y'),(v4.id,'Y')]
        account = self.user.get_profile()
        account.save_answers(save1_list)
        save2_list = [ (v2.id,'N'),(v3.id,'N'),(v5.id,'Y'),(v6.id,'Y')]
        account.save_answers(save2_list)
        get_list = account.get_answers()
        self.assertEqual(save2_list, get_list)
        
        
class ProfileTests(TestCase):

    def test_unicode(self):
        profile = Profile.objects.create(name='test')
        self.assertEquals(profile.name,str(profile))

    def test_get_answers(self):
        v1 = Variable.objects.create(name='v1', ask=False)
        v2 = Variable.objects.create(name='v2', ask=False)
        v3 = Variable.objects.create(name='v3', ask=False)
        v4 = Variable.objects.create(name='v4', ask=False)
        profile = Profile.objects.create(name='test')
        save_list = [ (v1.id,'Y'), (v2.id,'Y'),(v3.id,'Y'),(v4.id,'Y')]
        for key,value in save_list:
            profile.profileanswer_set.create(variable_id=key, value=value)
        get_list = profile.get_answers()
        self.assertEqual(save_list, get_list)

class SignalCreateAccount(TestCase):

    def setUp(self):
        signals.post_save.disconnect(create_account, sender=User)

    def tearDown(self):
        signals.post_save.connect(create_account, sender=User)

    def test_create_account(self):
        print 'test_create_account'
        username = random_string(10)
        email = '%s@test.com' % random_string(10)
        password =  User.objects.make_random_password(10)
        user = User.objects.create_user(username,email,password)
        self.assertRaises(Account.DoesNotExist, lambda: user.get_profile())
        create_account(None, user, False)
        self.assertRaises(Account.DoesNotExist, lambda: user.get_profile())
        create_account(None, user, True)
        self.assertTrue(isinstance(user.get_profile(),Account))

class SignalCreateTestUser(TestCase):

    def test_create_testuser(self):
        from django.conf import settings
        settings.DEBUG = True
        username = 'admin_test'
        password =  User.objects.make_random_password(10)
        dbconfig = settings.DATABASES['default']
        dbconfig['USER'] = username
        dbconfig['PASSWORD'] = password
        create_testuser(None,None,0)
        user = User.objects.get(username=username)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
