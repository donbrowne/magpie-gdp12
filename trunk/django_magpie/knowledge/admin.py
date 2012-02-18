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

admin.site.register(Fact, FactAdmin)
admin.site.register(Question)
admin.site.register(Recommend, RecsAdmin)
admin.site.register(ResourceFile)
