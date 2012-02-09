from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from knowledge.models import Question,Recommend,Rule


# TODO move logic into models
def index(request):
    if request.method == 'POST':
        # get list of answers from post from
        items = request.POST.items() 
        answers = []
        for name,value in items:
            if name.startswith('answer_'):
                qid = int(name[len('answer_'):])
                istrue = value == 'y'
                answers.append((qid, istrue))
        # prune rules based on answers
        rule_ids = map(int, request.session['rule_ids'])
        rule_list = Rule.objects.filter(id__in=rule_ids)
        match_rules = []
        for rule in rule_list:
            match_all = True
            for ranswer in rule.ruleanswer_set.all():
                expect = (ranswer.question.id, ranswer.answer)
                if expect not in answers:
                    match_all = False
                    break
            if match_all:
                match_rules.append(rule)
        # update recommend list, get next questions
        rec_ids = map(int, request.session['rec_ids'])
        rec_list = list(Recommend.objects.filter(id__in=rec_ids))
        question_list = []
        rule_ids = []
        for rule in match_rules:
            for rec in rule.recommends.all():
                if rec not in rec_list:
                    rec_list.append(rec)
                    rec_ids.append(rec.id)
            for child_rule in rule.rule_set.all():
                rule_ids.append(child_rule.id)
                for ranswer in child_rule.ruleanswer_set.all():
                    if ranswer.question not in question_list:
                        question_list.append(ranswer.question)
        if len(rule_ids) == 0:
            # all done
            del request.session['rule_ids']
            del request.session['rec_ids']
            return render_to_response(
                'knowledge/index.html', 
                {'recommend_list': rec_list},
                context_instance=RequestContext(request))
        else:
            # keep going
            request.session['rule_ids'] = map(str,rule_ids)
            request.session['rec_ids'] = map(str,rec_ids)
            return render_to_response(
                'knowledge/index.html', 
                { 'question_list': question_list,
                  'recommend_list': rec_list},
                context_instance=RequestContext(request))

    else:
        rule_list = Rule.objects.filter(requires__isnull=True)
        rule_ids = []
        question_list = []
        for rule in rule_list:
            rule_ids.append(rule.id)
            for ranswer in rule.ruleanswer_set.all():
                if ranswer.question not in question_list:
                    question_list.append(ranswer.question)
        request.session['rule_ids'] = map(str,rule_ids)
        request.session['rec_ids'] = []
        return render_to_response(
            'knowledge/index.html', 
            {'question_list': question_list},
             context_instance=RequestContext(request))
