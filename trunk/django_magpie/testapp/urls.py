from django.conf.urls.defaults import patterns, include, url
    
urlpatterns = patterns('testapp.views',
   # url(r'^add_rule/(?P<ruleset_id>\d+)/$', 'add_rule', name="add_rule"),
    url(r'^$', 'index'),
    url(r'^ask$', 'ask'),
    url(r'^done$', 'done'),
    url(r'^state$', 'saved', name='saved'),
)
