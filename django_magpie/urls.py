from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^$', 'knowledge.views.index', name='index'),
    url(r'^knowledge/', include('knowledge.urls')),
    url(r'^register/', include('register.urls')),
    #url(r'^django_magpie/', include('django_magpie.foo.urls')),
    url(r'^favicon\.ico$',  'django.views.generic.simple.redirect_to',  {'url': settings.STATIC_URL+'img/favicon.ico'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
