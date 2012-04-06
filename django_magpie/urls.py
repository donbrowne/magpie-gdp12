from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^$', 'knowledge.views.index', name='index'),
    url(r'^knowledge/', include('knowledge.urls')),
    url(r'^register/', include('register.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
