from django.conf.urls.defaults import patterns, include, url
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='login'),
)

urlpatterns += patterns('register.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^account/$', 'account', name='account'),
)

urlpatterns += patterns('knowledge.views',
    url(r'^logout/$', 'logout_view', name='logout'),
)
