from django import forms
from models import Account

class AccountForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    first_name = forms.CharField(label='first name', max_length=30)
    last_name = forms.CharField(label='last name', max_length=30)
    email = forms.EmailField(label='email',help_text='')

    class Meta:
        model = Account
        fields = ('profile',)

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.email = self.cleaned_data['email']
        u.save()
        account = super(AccountForm, self).save(*args,**kwargs)
        return account
