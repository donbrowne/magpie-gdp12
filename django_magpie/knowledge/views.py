from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response,redirect
#from knowledge.models import FactState, start_state, get_answers, recSummaryClosure
from knowledge.models import Engine,start_state,state_encode,state_decode,recSummaryClosure
from django.conf import settings
from django.contrib.auth.decorators import login_required
import subprocess 
import os
import pydot

# note sesson is a gui state so
# should not pass to business logic layer
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

def generatePmlGraph(request):
    pmlPath = request.GET.items()[0][1]
    if pmlPath.find("../") != -1:
        print ("[ERROR] '../' contained in specified file name, relative paths unallowed for security reasons")
        return None
    fullPath = settings.MEDIA_ROOT + pmlPath
    if os.path.isfile(fullPath):
        traverse = subprocess.Popen([settings.TRAVERSE_PATH,'-R','-L',fullPath],stdout=subprocess.PIPE)
        dotDesc = traverse.communicate()[0]
        graph = pydot.graph_from_dot_data(dotDesc)
        png = graph.create_png()
        return HttpResponse(png, mimetype="image/png")
    else:
        print ("[ERROR] File does not exist")
        return None


# TODO move this to questions url
def index(request):
    context = RequestContext(request)
    if request.method == 'POST':
        del_state(request.session)
        return redirect('knowledge/ask')
    return render_to_response('knowledge/index.html', context)

@login_required
def saved(request):
    context = RequestContext(request)
    state = start_state(request.user)
    profile = request.user.get_profile()
    state.next_state(profile.get_answers())
    return render_to_response('knowledge/saved.html', {
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
            'knowledge/done.html', {
                'recommend_list': recommends,
                'reason_list' : reasons,
                'nonRecommendedList' : nonRecommended,
                'reasonsNonList': reasonsNon,
                'unansweredList' : unansweredReasons
            },
            context)
    # keep going
    return render_to_response(
        'knowledge/ask.html', {
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
    
