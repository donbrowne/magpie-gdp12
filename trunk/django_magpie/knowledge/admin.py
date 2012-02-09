from knowledge.models import *
from django.contrib import admin

class FactAnswerInline(admin.TabularInline):
    model = FactAnswer

class FactAdmin(admin.ModelAdmin):
    filter_horizontal = ('requires','recommends',)
    inlines = [FactAnswerInline]

admin.site.register(Fact, FactAdmin)
admin.site.register(Question)
admin.site.register(Recommend)
