from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from models import Account

class AccountForm(forms.ModelForm):

    username = forms.CharField(
            label='Username', 
            max_length=30, 
            widget=forms.TextInput(
                attrs={
                    'disabled':'disabled'
                }),required=False)
    first_name = forms.CharField(label='First name', max_length=30, required=False)
    last_name = forms.CharField(label='last name', max_length=30, required=False)
    email = forms.EmailField(label='email',help_text='',required=False)

    class Meta:
        model = Account
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    # we call this because post form does not contain disabled field data
    def reload_disabled(self):
        self.fields['username'].widget.value_from_datadict = lambda *args: self.instance.user.username
    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.user.username
        else:
            return self.cleaned_data.get('username', None)

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        u.save()
        account = super(AccountForm, self).save(*args,**kwargs)
        return account

class RegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Re-enter Password"), widget=forms.PasswordInput)
    email = forms.EmailField(label=_("E-mail"), max_length=75, required=False)

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
