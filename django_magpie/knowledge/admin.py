from django.contrib import admin
from django import forms
from django.db import models
from models import Variable,Recommend,RuleSet,Rule,RulePremise,RuleConclusion,RuleRecommend
from models import ExternalLink,ResourceFile
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.conf.urls.defaults import patterns
from django.utils.encoding import iri_to_uri
from django.contrib.admin.util import unquote
from django.utils import html


class ExtLinkInline(admin.TabularInline):
    model = ExternalLink

class RecsAdmin(admin.ModelAdmin):
    inlines = [ExtLinkInline]
    
class ResourceFileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.last_modified_by = request.user
        obj.save()
        
    def queryset(self, request):
        qs = super(ResourceFileAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('owner',)
        return super(ResourceFileAdmin, self).add_view(request, form_url, extra_context)
        
    def change_view(self, request, form_url='', extra_context=None):
        self.exclude = None
        return super(ResourceFileAdmin, self).change_view(request, form_url, extra_context)


# django snippet 2673
class ButtonAdmin(admin.ModelAdmin):
    change_buttons=[]
    list_buttons=[]

    def button_view_dispatcher(self, request, url):
        # Dispatch the url to a function call
        if url is not None:
            import re
            res = re.match('(.*/)?(?P<id>\d+)/(?P<command>.*)', url)
            if res:
                if res.group('command') in [b.func_name for b in self.change_buttons]:
                    obj = self.model._default_manager.get(pk=res.group('id'))
                    response = getattr(self, res.group('command'))(request, obj)
                    if response is None:
                        from django.http import HttpResponseRedirect
                        return HttpResponseRedirect(request.META['HTTP_REFERER'])
                    return response
            else:
                res = re.match('(.*/)?(?P<command>.*)', url)
                if res:
                    if res.group('command') in [b.func_name for b in self.list_buttons]:
                        response = getattr(self, res.group('command'))(request)
                        if response is None:
                            from django.http import HttpResponseRedirect
                            return HttpResponseRedirect(request.META['HTTP_REFERER'])
                        return response
        # Delegate to the appropriate method, based on the URL.
        from django.contrib.admin.util import unquote
        if url is None:
            return self.changelist_view(request)
        elif url == "add":
            return self.add_view(request)
        elif url.endswith('/history'):
            return self.history_view(request, unquote(url[:-8]))
        elif url.endswith('/delete'):
            return self.delete_view(request, unquote(url[:-7]))
        else:
            return self.change_view(request, unquote(url))

    def get_urls(self):
        from django.conf.urls.defaults import url, patterns
        from django.utils.functional import update_wrapper
        # Define a wrapper view
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        #  Add the custom button url
        urlpatterns = patterns('',
            url(r'^(.+)/$', wrap(self.button_view_dispatcher),)
        )
        return urlpatterns + super(ButtonAdmin, self).get_urls()

    def change_view(self, request, object_id, extra_context=None):
        if not extra_context: extra_context = {}
        if hasattr(self, 'change_buttons'):
            extra_context['buttons'] = self._convert_buttons(self.change_buttons)
        if '/' in object_id:
            object_id = object_id[:object_id.find('/')]
        return super(ButtonAdmin, self).change_view(request, object_id, extra_context)

    def changelist_view(self, request, extra_context=None):
        if not extra_context: extra_context = {}
        if hasattr(self, 'list_buttons'):
            extra_context['buttons'] = self._convert_buttons(self.list_buttons)
        return super(ButtonAdmin, self).changelist_view(request, extra_context)

    def _convert_buttons(self, orig_buttons):
        buttons = []
        for b in orig_buttons:
            buttons.append({ 'func_name': b.func_name, 'short_description': b.short_description })
        return buttons

YN_CHOICES = (
    (True, "Yes"),
    (False, "No")
)
    
class RuleRecommendInline(admin.TabularInline):
    model = RuleRecommend
    extra = 0
    verbose_name_plural = "RECOMMENDATIONS"
    template = 'admin/knowledge/edit_inline/tabular.html'

class RuleConclusionInline(admin.TabularInline):
    model = RuleConclusion
    extra = 0
    verbose_name_plural = "CONCLUSIONS"
    template = 'admin/knowledge/edit_inline/tabular.html'

class RulePremiseInline(admin.TabularInline):
    model = RulePremise
    extra = 0
    verbose_name_plural = "PREMISES"
    template = 'admin/knowledge/edit_inline/tabular.html'


class RuleForm(forms.ModelForm):
     parent = forms.ModelChoiceField(label="",queryset=RuleSet.objects.all(), widget=forms.HiddenInput())
     #hidden_fields = ('parent','order',)

class RuleAdmin(admin.ModelAdmin):
    inlines = [RulePremiseInline, RuleConclusionInline, RuleRecommendInline]
    exclude = ('order',)

    def add_view(self, request, form_url='', extra_context=None):
        result = super(RuleAdmin, self).add_view(request, form_url, extra_context)
        if request.POST:
            if 'parent' in request.POST:
                parent= request.POST['parent']
                result['Location'] = iri_to_uri("/admin/knowledge/ruleset/%s" % parent)
        return result

    def change_view(self, request, object_id, extra_context=None):
        result = super(RuleAdmin, self).change_view(request, object_id, extra_context)
        obj = self.get_object(request, unquote(object_id))
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'): 
            result['Location'] = iri_to_uri("/admin/knowledge/ruleset/%s" % obj.parent_id)
        return result
    
class RuleInline(admin.TabularInline):
    model = Rule
    extra = 0
    max_num = 0
    fields = ('order', 'details')
    def details(self, obj):
        astr = mark_safe(u'<a href="edit_rule/%d">%s</a>' % (obj.id, obj.get_dets()))
        return astr
    template = 'admin/knowledge/edit_inline/tabular.html'
    readonly_fields = ('details',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        form_field = super(RuleInline,self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'order':
            form_field.widget.attrs.update({'readonly':  'readonly'} )
        return form_field

    class Media: 
        js = (
            'js/jquery-1.5.1.min.js',
            'js/jquery-ui-1.8.11.custom.min.js',
            'js/menu-sort.js'
        )


class RuleSetAdmin(ButtonAdmin):
    inlines = [RuleInline]

    def get_urls(self):
        urls = super(RuleSetAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<ruleset_id>\d+)/edit_rule/(?P<rule_id>\d+)/$', self.admin_site.admin_view(self.edit_rule))
        )
        return my_urls + urls

    def add_rule(self, request, ruleset):
        if request.method == 'GET':
            initial = dict(request.GET.items())
            initial['parent']  = ruleset.pk
            request.GET = initial
        admin = RuleAdmin(Rule, self.admin_site)
        admin.form = RuleForm
        return admin.add_view(request)

    def edit_rule(self, request, ruleset_id, rule_id):
        admin = RuleAdmin(Rule, self.admin_site)
        admin.form = RuleForm
        return admin.change_view(request, rule_id)

    add_rule.short_description = 'Add rule'

    change_buttons = [ add_rule ]

class ExtLinkInline(admin.TabularInline):
    model = ExternalLink

class RecsAdmin(admin.ModelAdmin):
    inlines = [ExtLinkInline]

class VariableAdmin(admin.ModelAdmin):
    list_display = ['name', 'ask','prompt']


admin.site.register(ResourceFile, ResourceFileAdmin)
admin.site.register(Recommend, RecsAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(RuleSet, RuleSetAdmin)

