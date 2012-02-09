from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from knowledge.models import Question,Recommend,Rule

def get_ids(alist):
    return map(lambda elem:elem.id, alist)

# update recommends + calculate next set of questions
def next_sess(rule_ids, answers, rec_ids):
    # build list of rules that match all answers
    rules = []
    questions = []
    recommends = list(Recommend.objects.filter(id__in=rec_ids))
    for rule in Rule.objects.filter(id__in=rule_ids):
        # check if expected answers match those given
        match_all = True
        for ranswer in rule.ruleanswer_set.all():
            expect = (ranswer.question.id, ranswer.answer)
            if expect not in answers:
                match_all = False
                break
        if match_all:
            for recommend in rule.recommends.all():
                if recommend not in recommends:
                    recommends.append(recommend)
            for child_rule in rule.rule_set.all():
                if child_rule not in rules:
                    rules.append(child_rule)
                for ranswer in child_rule.ruleanswer_set.all():
                    if ranswer.question not in questions:
                        questions.append(ranswer.question)
    return rules, questions, recommends

# start a q+a session
def start_sess():
    rules = []
    questions = []
    recommends = []
    for rule in Rule.objects.filter(requires__isnull=True):
        if rule not in rules:
            rules.append(rule)
        for ranswer in rule.ruleanswer_set.all():
            if ranswer.question not in questions:
                questions.append(ranswer.question)
    return rules, questions

def get_answers(items):
    answers = []
    for name,value in items:
        if name.startswith('answer_'):
            qid = int(name[len('answer_'):])
            istrue = value == 'y'
            answers.append((qid, istrue))
    return answers

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
