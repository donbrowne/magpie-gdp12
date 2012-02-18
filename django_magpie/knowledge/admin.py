from knowledge.models import *
from django.contrib import admin

class FactQuestionInline(admin.TabularInline):
    model = FactQuestion

class FactAdmin(admin.ModelAdmin):
    filter_horizontal = ('requires','recommends',)
    inlines = [FactQuestionInline]

admin.site.register(Fact, FactAdmin)
admin.site.register(Question)
admin.site.register(Recommend)
admin.site.register(ResourceFile)
