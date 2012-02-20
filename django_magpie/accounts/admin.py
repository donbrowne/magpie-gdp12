from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import UserProfile, UserAnswer, UserType

class UserTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ('facts',)

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('types',)
    inlines = [UserAnswerInline]
    readonly_fields = ('user',)
    fields = ('user','types')
        

"""
class UserProfileInline(admin.StackedInline):
    filter_horizontal = ('facts',)
    inlines = [UserAnswerInline]
    model = UserProfile
    fk_name = 'user'
    max_num = 1

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline,]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
"""

admin.site.register(UserType,  UserTypeAdmin)
admin.site.register(UserProfile,  UserProfileAdmin)
