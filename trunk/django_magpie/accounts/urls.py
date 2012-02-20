from django.conf.urls.defaults import patterns, include, url
#from django.contrib.auth.views import login, logout

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

urlpatterns += patterns('accounts.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^profile/$', 'profile', name='profile'),
)
