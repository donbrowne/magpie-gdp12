from knowledge.models import *
from django.contrib import admin

class RuleAnswerInline(admin.TabularInline):
    model = RuleAnswer

class RuleAdmin(admin.ModelAdmin):
    filter_horizontal = ('requires','recommends',)
    inlines = [RuleAnswerInline]

admin.site.register(Rule, RuleAdmin)
admin.site.register(Question)
admin.site.register(Recommend)
