from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('knowledge.views',
    url(r'^$', 'index'),
    url(r'^ask$', 'ask'),
    url(r'^done$', 'done'),
    url(r'^state$', 'saved', name='saved'),
   # url(r'^logout$', 'logout_view', name='logout_view'),
    (r'^pmlGraph/', 'generatePmlGraph'),
    (r'^pmlView/', 'generatePmlGraphHtml'),
)
