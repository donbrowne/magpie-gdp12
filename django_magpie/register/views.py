# Create your views here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login
from django.contrib import messages

from forms import AccountForm,RegistrationForm

def register(request):
    redirect_to = request.REQUEST.get('next', '')
    context = RequestContext(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect(redirect_to)
    else:
        form = RegistrationForm()
    return render_to_response("registration/register.html", {
        'form': form,
        'next': redirect_to,
    }, context)

@login_required
def account(request):
    redirect_to = request.REQUEST.get('next', '')
    user = request.user
    account = user.account
    if request.method == 'POST': # If the form has been submitted...
        if 'cancel' not in request.POST:
            form = AccountForm(request.POST,instance=account) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()
                messages.info(request, "Account updated.")
                return HttpResponseRedirect(redirect_to)
            else:
                form.reload_disabled()
    else:
        user = request.user
        account = user.account
        form = AccountForm(instance=account) # An unbound form
    return render_to_response('registration/edit_profile.html', {
                'form': form,
                'next': redirect_to,
                }, context_instance=RequestContext(request))

