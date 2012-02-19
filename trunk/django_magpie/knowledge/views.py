from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response,redirect
from knowledge.models import FactState, start_state, get_answers, generateRecSummary

# note sesson is a gui state so
# should not pass to business logic layer
def del_state(session):
    for key in ['test_ids','pass_ids','answers','falseFactIDs']:
        if key in session:
            del session[key]

def get_state(session):
    test_ids = session['test_ids']
    pass_ids = session['pass_ids']
    answers = session['answers']
    falseFactIDs = session['falseFactIDs']
    return FactState(test_ids, pass_ids, answers, falseFactIDs)

def put_state(session, state):
    session['test_ids'] = state.test_ids
    session['pass_ids'] = state.pass_ids
    session['answers'] = state.answers
    session['falseFactIDs'] = state.falseFactIDs

# TODO move this to questions url
def index(request):
    context = RequestContext(request)
    if request.method == 'POST':
        del_state(request.session)
        return redirect('knowledge/ask')
    return render_to_response('knowledge/index.html', context)

def ask(request):
    context = RequestContext(request)
    if request.method == 'POST':
        answers =  get_answers(request.POST.items())
        state = get_state(request.session)
        state = state.next_state(answers)
        questions = state.get_questions()
        recommends = map(generateRecSummary,state.get_recommends())
        print recommends[0].links
        nonRecommended = state.getNonRecommended()
        reasons = state.get_reasons()
        reasonsNon = state.getNonReasons()
        unansweredReasons = state.getUnansweredReasons()
        if len(questions) == 0:
            # all done
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
        put_state(request.session, state)
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
    state = start_state()
    put_state(request.session, state)
    questions = state.get_questions()
    if len(questions) == 0:
        # all done
        return render_to_response(
                'knowledge/done.html', {
                    'recommend_list': recommends,
                    'reason_list' : reasons,
                    'nonRecommendedList' : nonRecommended,
                    'reasonsNonList': reasonsNon,
                    'unansweredList' : unansweredReasons
                },
                context)
    return render_to_response(
        'knowledge/ask.html', {
        'question_list': state.get_questions()
        },
        context)

# save state here if logged in (else keep in cookie)
def done(request):
    return redirect('/')
    
