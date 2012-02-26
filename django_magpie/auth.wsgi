import os 
import sys

sys.path.append('PATH/django_magpie')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db

def check_password(environ, user, password):
   db.reset_queries()
   kwargs = {'username': user, 'is_active': True} 
   try: 
       try: 
           user = User.objects.get(**kwargs) 
       except User.DoesNotExist: 
           return None

       if user.check_password(password): 
           return user.is_staff or user.has_perm('knowledge.restricted_access') or user.is_superuser
       else:
           return False
   finally: 
       db.connection.close() 
