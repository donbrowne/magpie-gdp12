# Create your views here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from forms import UserProfileForm

def register(request):
    redirect_to = request.REQUEST.get('next', '')
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(redirect_to)
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
        'next': redirect_to,
    }, context)

@login_required
def profile(request):
    redirect_to = request.REQUEST.get('next', '')
    user = request.user
    profile = user.userprofile
    if request.method == 'POST': # If the form has been submitted...
        if 'cancel' not in request.POST:
            form = UserProfileForm(request.POST,instance=profile) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()
        return HttpResponseRedirect(redirect_to)
    else:
        user = request.user
        profile = user.userprofile
        form = UserProfileForm(instance=profile) # An unbound form
    return render_to_response('registration/edit_profile.html', {
                'form': form,
                'next': redirect_to,
                }, context_instance=RequestContext(request))

