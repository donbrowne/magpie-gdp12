from knowledge.models import *
from django.contrib import admin

class RuleAdmin(admin.ModelAdmin):
    filter_horizontal = ('facts','recommendations',)

admin.site.register(Fact)
admin.site.register(Question)
admin.site.register(Recommendation)
admin.site.register(Rule, RuleAdmin)
