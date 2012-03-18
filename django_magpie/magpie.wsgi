import os
import sys
import django.core.handlers.wsgi

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
_app = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    os.environ['DJANGO_URL_ROOT'] = os.path.dirname(environ['SCRIPT_NAME'])
    return _app(environ, start_response)
