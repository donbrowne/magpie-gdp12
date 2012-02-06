from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from knowledge.models import Question

def index(request):
    question_list = Question.objects.all()
    return render_to_response('knowledge/index.html', {'question_list': question_list})
