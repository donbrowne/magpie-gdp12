from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from models import Account
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
        password1 =  User.objects.make_random_password(10)
        email = '%s@test.com' % random_string(10)

        rsp = self.client.post(self.reg_url, {
                'username': username,
                'password1': 'regtest',
                'password2': 'regtest',
                'email' : email
                })

        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp['Location'], 'http://testserver' + self.redirect)

        user = User.objects.get(username=username)
        self.assertEqual(user.username,username)
        self.assertEqual(user.email, email)
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

    def test_get_answers(self):
        pass
