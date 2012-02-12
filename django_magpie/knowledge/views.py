from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from knowledge.models import FactState, start_state, get_answers

# note sesson is a gui state so
# should not pass to business logic layer
def del_state(session):
    del session['test_ids']
    del session['pass_ids']
    del session['answers']
    del session['falseFactIDs']


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
        answers =  get_answers(request.POST.items())
        state = get_state(request.session)
        state = state.next_state(answers)
        questions = state.get_questions()
        recommends = state.get_recommends()
        nonRecommended = state.getNonRecommended()
        reasons = state.get_reasons()
        reasonsNon = state.getNonReasons()
        otherRecs = state.getOtherRecs()
        if len(questions) == 0:
            # all done
            del_state(request.session)
            return render_to_response(
                'knowledge/index.html', {
                    'recommend_list': recommends,
                    'reason_list' : reasons,
                    'nonRecommendedList' : nonRecommended,
                    'reasonsNonList': reasonsNon,
                    'otherRecsList' : otherRecs
                },
                context)
        else:
            # keep going
            put_state(request.session, state)
            return render_to_response(
                'knowledge/index.html', {
                  'question_list': questions,
                  'recommend_list': recommends,
                  'reason_list': reasons,
                  'nonRecommendedList': nonRecommended,
                  'reasonsNonList': reasonsNon,
                  'otherRecsList' : otherRecs
                },
                context)
    else:
        state = start_state()
        put_state(request.session, state)
        return render_to_response(
            'knowledge/index.html', {
                'question_list': state.get_questions()
            },
            context)
