from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('knowledge.views',
    url(r'^$', 'index'),
    url(r'^ask$', 'ask'),
    url(r'^reset$', 'reset', name='reset'),
    url(r'^state$', 'saved', name='saved'),
   # url(r'^logout$', 'logout_view', name='logout_view'),
    (r'^pmlView/', 'pmlView'),
)
