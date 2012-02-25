import os 
import sys

sys.path.append('/var/www/magpie-gdp12-read-only/django_magpie')
sys.path.append('/var/www/magpie-gdp12-read-only/django_magpie/knowledge')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django import db
from views import checkUserPermission

def check_password(environ, user, password):
   db.reset_queries()
   kwargs = {'username': user, 'is_active': True} 
   try: 
       try: 
           user = User.objects.get(**kwargs) 
       except User.DoesNotExist: 
           return None

       if user.check_password(password): 
           print environ
           print environ['REQUEST_URI']
           return checkUserPermission(environ['REQUEST_URI'],user.groups.all())
       else:
           return False
   finally: 
       db.connection.close() 
