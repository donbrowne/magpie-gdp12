import os
import sys

sys.path.append('/var/www/magpie-gdp12-read-only/django_magpie')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
