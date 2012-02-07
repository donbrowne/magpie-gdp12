from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from knowledge.models import Question,Rule,Fact,Recommendation

# TODO move logic into models
def index(request):
    if request.method == 'POST':
        # get list of answers from post form
        items = request.POST.items() 
        answers = []
        for name,value in items:
            if name.startswith('answer_'):
                qid = int(name[len('answer_'):])
                istrue = value == 'y'
                answers.append((qid, istrue))
        # convert answers to facts
        facts = []
        for qid,istrue in answers:
            question = Question.objects.get(id=qid)
            if question:
                if istrue:
                    facts.append(question.yes_fact)
                else:
                    facts.append(question.no_fact)
        # match facts to rules
        rules = []
        for rule in Rule.objects.all():
            match_all = True
            for fact in rule.facts.all():
                if fact not in facts:
                    match_all = False
                    break
            if match_all:
                rules.append(rule)
        # now build list of recommendations
        rec_list = []
        for rule in rules:
            for rec in rule.recommendations.all():
                if rec not in rec_list:
                    rec_list.append(rec)
        # convert to string
        text_list = []
        for rec in rec_list:
            text_list.append(rec.text)
        return HttpResponse("Thank you for your answers. Recommendations=%s" % ','.join(text_list))
    else:
        question_list = Question.objects.all()
        return render_to_response(
            'knowledge/index.html', 
            {'question_list': question_list},
             context_instance=RequestContext(request))
