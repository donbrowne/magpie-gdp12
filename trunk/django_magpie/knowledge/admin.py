from knowledge.models import *
from django.contrib import admin

class FactQuestionInline(admin.TabularInline):
    model = FactQuestion

class FactAdmin(admin.ModelAdmin):
    filter_horizontal = ('requires','recommends',)
    inlines = [FactQuestionInline]

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

admin.site.register(Question)
admin.site.register(ResourceFile, ResourceFileAdmin)
admin.site.register(Recommend, RecsAdmin)
admin.site.register(Fact, FactAdmin)
