from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from knowledge.models import Question,Recommend,Fact


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
        # prune facts based on answers
        fact_ids = map(int, request.session['fact_ids'])
        fact_list = Fact.objects.filter(id__in=fact_ids)
        match_facts = []
        for fact in fact_list:
            match_all = True
            for fanswer in fact.factanswer_set.all():
                expect = (fanswer.question.id, fanswer.answer)
                if expect not in answers:
                    match_all = False
                    break
            if match_all:
                match_facts.append(fact)
        # update recommend list, get next questions
        rec_ids = map(int, request.session['rec_ids'])
        rec_list = list(Recommend.objects.filter(id__in=rec_ids))
        question_list = []
        fact_ids = []
        for fact in match_facts:
            for rec in fact.recommends.all():
                if rec not in rec_list:
                    rec_list.append(rec)
                    rec_ids.append(rec.id)
            for child_fact in fact.fact_set.all():
                fact_ids.append(child_fact.id)
                for fanswer in child_fact.factanswer_set.all():
                    if fanswer.question not in question_list:
                        question_list.append(fanswer.question)
        if len(fact_ids) == 0:
            # all done
            del request.session['fact_ids']
            del request.session['rec_ids']
            return render_to_response(
                'knowledge/index.html', 
                {'recommend_list': rec_list},
                context_instance=RequestContext(request))
        else:
            # keep going
            request.session['fact_ids'] = map(str,fact_ids)
            request.session['rec_ids'] = map(str,rec_ids)
            return render_to_response(
                'knowledge/index.html', 
                { 'question_list': question_list,
                  'recommend_list': rec_list},
                context_instance=RequestContext(request))

    else:
        fact_list = Fact.objects.filter(requires__isnull=True)
        fact_ids = []
        question_list = []
        for fact in fact_list:
            fact_ids.append(fact.id)
            for fanswer in fact.factanswer_set.all():
                if fanswer.question not in question_list:
                    question_list.append(fanswer.question)
        request.session['fact_ids'] = map(str,fact_ids)
        request.session['rec_ids'] = []
        return render_to_response(
            'knowledge/index.html', 
            {'question_list': question_list},
             context_instance=RequestContext(request))
