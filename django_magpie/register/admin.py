from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from models import Profile, ProfileAnswer, Account, AccountAnswer

class ProfileAnswerInline(admin.TabularInline):
    model = ProfileAnswer
    extra = 0
    
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileAnswerInline]


class AccountAnswerInline(admin.TabularInline):
    model = AccountAnswer
    extra = 0

class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountAnswerInline]
    readonly_fields = ('user',)

admin.site.register(Profile,  ProfileAdmin)
admin.site.register(Account,  AccountAdmin)
