# Create your views here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

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