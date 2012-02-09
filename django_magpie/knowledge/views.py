from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from knowledge.models import start_sess,next_sess,get_ids,get_answers

# TODO move logic into models
def index(request):
    if request.method == 'POST':
        # extract session state
        answers =  get_answers(request.POST.items())
        rule_ids = request.session['rule_ids']
        rec_ids = request.session['rec_ids']
        # establish next state
        rules,questions,recommends = next_sess(rule_ids, answers, rec_ids)
        if len(rule_ids) == 0:
            # all done
            del request.session['rule_ids']
            del request.session['rec_ids']
            return render_to_response(
                'knowledge/index.html', 
                {'recommend_list': recommends },
                context_instance=RequestContext(request))
        else:
            # keep going
            request.session['rule_ids'] = get_ids(rules)
            request.session['rec_ids'] = get_ids(recommends)
            return render_to_response(
                'knowledge/index.html', 
                { 'question_list': questions,
                  'recommend_list': recommends},
                context_instance=RequestContext(request))

    else:
        rule_ids,questions = start_sess()
        request.session['rule_ids'] = get_ids(rule_ids)
        request.session['rec_ids'] = []
        return render_to_response(
            'knowledge/index.html', 
            {'question_list': questions },
             context_instance=RequestContext(request))
