from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response,redirect
#from testapp.models import Engine, start_state, get_answers, recSummaryClosure
from knowledge.models import recSummaryClosure
from testapp.models import Engine,start_state,state_encode,state_decode
from django.conf import settings
from django.contrib.auth.decorators import login_required
import subprocess 
import os
import pydot

from django.http import HttpResponse
from models import Engine

def get_answers(items):
    answers = []
    for name,value in items:
        if name.startswith('answer_'):
            qid = int(name[len('answer_'):])
            istrue = value == 'y'
            answers.append((qid, istrue))
    return answers

def del_state(session):
    try:
      del session['engine']
    except KeyError:
      pass

def put_state(session, state):
    session['engine'] = state_encode(state) 

def get_state(session):
    if 'engine' in session:
        slist = session['engine']
    else:
        slist = []
    return state_decode(slist) 

# TODO move this to questions url
def index(request):
    context = RequestContext(request)
    if request.method == 'POST':
        del_state(request.session)
        return redirect('testapp/ask')
    return render_to_response('testapp/index.html', context)

@login_required
def saved(request):
    context = RequestContext(request)
    state = start_state(request.user)
    profile = request.user.get_profile()
    state = state.next_state(profile.get_answers())
    return render_to_response('testapp/saved.html', {
                'recommend_list': state.get_recommends(),
                'reason_list' : state.get_reasons(),
                'nonRecommendedList' : state.getNonRecommended(),
                'reasonsNonList': state.getNonReasons(),
                'unansweredList' : state.getUnansweredReasons()
                }, context)

def ask_or_done(request, state):
    context = RequestContext(request)
    questions = state.get_questions()
    summaryClosure = recSummaryClosure(request.user)
    recommends = map(summaryClosure,state.get_recommends())
    nonRecommended = state.getNonRecommended()
    reasons = state.get_reasons()
    reasonsNon = state.getNonReasons()
    unansweredReasons = state.getUnansweredReasons()
    put_state(request.session, state)
    # check if all done
    if len(questions) == 0:
        return render_to_response(
            'testapp/done.html', {
                'recommend_list': recommends,
                'reason_list' : reasons,
                'nonRecommendedList' : nonRecommended,
                'reasonsNonList': reasonsNon,
                'unansweredList' : unansweredReasons
            },
            context)
    # keep going
    return render_to_response(
        'testapp/ask.html', {
        'question_list': questions,
        'recommend_list': recommends,
        'reason_list': reasons,
        'nonRecommendedList': nonRecommended,
        'reasonsNonList': reasonsNon,
        'unansweredList' : unansweredReasons
        },
        context)


def ask(request):
    context = RequestContext(request)
    if request.method == 'POST':
        # user answered some questions
        answers =  get_answers(request.POST.items())
        state = get_state(request.session)
        state.next_state(answers)
        rsp = ask_or_done(request, state)
    else:
        # first time
        state = start_state(request.user)
        state.next_state()
        rsp = ask_or_done(request, state)
    return rsp

# save state here if logged in (else keep in cookie)
def done(request):
    if request.user.is_authenticated():
        # save answers for authenticated users.
        state = get_state(request.session)
        profile = request.user.get_profile()
        profile.save_answers(state.get_answers())
    else:
        # Do something for anonymous users.
        pass
    return redirect('/')

