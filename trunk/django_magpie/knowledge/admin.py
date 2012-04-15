from django.contrib import admin
from django import forms
#from django.db import models

from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect,HttpResponse
from django.conf.urls.defaults import patterns
from django.utils.encoding import iri_to_uri
from django.contrib.admin.util import unquote
from django.utils import html
from django.utils.html import escape, escapejs
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import BaseInlineFormSet

from models import Variable,Recommend
from models import RuleSet,Rule,RulePremise,RuleConclusion,RuleRecommend
from models import ExternalLink,ResourceFile
from models import PremiseParser,PremiseException

class ExtLinkInline(admin.TabularInline):
    model = ExternalLink

class RecsAdmin(admin.ModelAdmin):
    inlines = [ExtLinkInline]

#Instance methods unit tested.
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

class RulePremiseFormSet(BaseInlineFormSet):

   def clean(self): 
      super(RulePremiseFormSet, self).clean()
      if any(self.errors):
          return
      # first rip data from post data
      premise_list = []
      for i in range(0, self.total_form_count()):
          form = self.forms[i]
          # ignore an extra form and hasn't changed
          if i >= self.initial_form_count() and not form.has_changed():
              continue
          variable = form.cleaned_data.get('variable', None)
          value = form.cleaned_data.get('value', '')
          lchoice = form.cleaned_data.get('lchoice', '')
          rchoice = form.cleaned_data.get('rchoice', '')
          premise = RulePremise()
          if variable:
              premise.variable = variable
          premise.value = value
          premise.lchoice = lchoice
          premise.rchoice = rchoice
          premise_list.append(premise)
      # no premises -> no check
      if len(premise_list) == 0:
          return
      # now check if sane
      parser = PremiseParser()
      try:
          parser.parse(premise_list)
      except PremiseException as e:
          pos = e.pos + 1
          reason = e.reason
          if e.pos < len(self._errors):
              # set the error message for the form that caused it
              form_errors = self._errors[e.pos]
              form_errors[e.field_name] = self.error_class([reason])
          raise forms.ValidationError("At line %d: %s" %(pos,reason))

class RulePremiseInline(admin.TabularInline):
    model = RulePremise
    formset = RulePremiseFormSet
    extra = 0
    verbose_name_plural = "PREMISES"
    fields = ('lchoice', 'variable','value', 'rchoice')
    #exclude = ('lchoice','rchoice')
    #form = PremiseForm
    #template = 'admin/knowledge/edit_inline/tabular.html'

    def formfield_for_dbfield(self, db_field, **kwargs):
        form_field = super(RulePremiseInline,self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name in [ 'lchoice', 'rchoice' ]:
            form_field.widget.attrs = { 'size' : 10 }
        return form_field


class RuleRecommendInline(admin.TabularInline):
    model = RuleRecommend
    extra = 0
    verbose_name_plural = "RECOMMENDATIONS"

class RuleConclusionInline(admin.TabularInline):
    model = RuleConclusion
    extra = 0
    verbose_name_plural = "CONCLUSIONS"

class RuleAdmin(admin.ModelAdmin):

    inlines = [RulePremiseInline, RuleConclusionInline, RuleRecommendInline]
    exclude = ('order',)

    def __init__(self, model, admin_site, ruleset=None):
        super(RuleAdmin, self).__init__(model, admin_site)
        self.ruleset = ruleset

    def get_model_perms(self, request):
        return {}

    def response_change(self, request, obj):
        if "_popup" in request.POST:
            pk_value = obj._get_pk_val()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        return super(RuleAdmin, self).response_change(request, obj, *args, **kwargs)


    def save_model(self, request, obj, form, change):
        if not change:
            obj.parent  = self.ruleset
        obj.save()
    
class RuleInline(admin.TabularInline):
    model = Rule
    extra = 0
    max_num = 0
    fields = ('order', 'details')
    def details(self, obj):
        astr = mark_safe(u'<a onclick=\'return showAddAnotherPopup(this);\' href="edit_rule/%d">%s</a>' % (obj.id, obj.get_dets()))
        return astr
    #template = 'admin/knowledge/edit_inline/tabular.html'
    readonly_fields = ('details',)
    sortable_field_name = "order"

    class Media: 
         js = (
           'js/menu-sort.js',
         )


class RuleSetAdmin(admin.ModelAdmin):
    inlines = [RuleInline]

    def get_urls(self):
        urls = super(RuleSetAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<ruleset_id>\d+)/add_rule/$', self.admin_site.admin_view(self.add_rule)),
            (r'^(?P<ruleset_id>\d+)/edit_rule/(?P<rule_id>\d+)/$', self.admin_site.admin_view(self.edit_rule))
        )
        return my_urls + urls
 
    def add_rule(self, request, ruleset_id):
        ruleset = get_object_or_404(RuleSet, pk=int(ruleset_id))
        admin = RuleAdmin(Rule, self.admin_site, ruleset)
        return admin.add_view(request)

    def edit_rule(self, request, ruleset_id, rule_id):
        admin = RuleAdmin(Rule, self.admin_site, None)
        return admin.change_view(request, rule_id)

class ExtLinkInline(admin.TabularInline):
    model = ExternalLink

class RecsAdmin(admin.ModelAdmin):
    inlines = [ExtLinkInline]

class VariableAdminForm(forms.ModelForm):

    class Meta:
        model = Variable

    def clean(self):
        cleaned_data = super(VariableAdminForm, self).clean()
        ask = cleaned_data.get('ask')
        prompt = cleaned_data.get('prompt')
        if ask and not prompt:
             self._errors['prompt'] = self.error_class([u"Prompt must be set"])
        return cleaned_data

class VariableAdmin(admin.ModelAdmin):
    list_display = ['name', 'ask','prompt']
    form = VariableAdminForm


admin.site.register(ResourceFile, ResourceFileAdmin)
admin.site.register(Recommend, RecsAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(Rule, RuleAdmin)

