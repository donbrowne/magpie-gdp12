from django.http import HttpResponse
from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response,redirect
from knowledge.models import Engine,start_state,state_encode,state_decode,recSummaryClosure
from django.conf import settings
from django.contrib.auth.decorators import login_required
import subprocess 
import os
import pydot
import libxml2
import libxslt
import tempfile

# note sesson is a gui state so
# should not pass to business logic layer
def get_answers(items):
    answers = []
    for name,value in items:
        if name.startswith('answer_'):
            qid = int(name[len('answer_'):])
            # hack to prevent python 2.6 coerce
            istrue = value == 'y'
            value = 'Y' if istrue else 'N'
            answers.append((qid, value))
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
      
def xmlToPml(filePath):
    pmlStyleDoc=libxml2.parseFile(settings.PML_PATH + "/xpml/xpml.xsl")
    style = libxslt.parseStylesheetDoc(pmlStyleDoc)
    try:
        doc = libxml2.parseFile(filePath)
        result = style.applyStylesheet(doc, None)
        return style.saveResultToString(result)
    except (libxml2.parserError, TypeError):
        return None
        
def xmlToRoadmap(filePath):
    pmlStyleDoc=libxml2.parseFile(settings.PML_PATH + "/xpml/pmldoc.xsl")
    style = libxslt.parseStylesheetDoc(pmlStyleDoc)
    try:
        doc = libxml2.parseFile(filePath)
        result = style.applyStylesheet(doc, None)
        return style.saveResultToString(result)
    except (libxml2.parserError, TypeError):
        return None
    
def pmlToDot(pml):
    if pml is None:
        return None
    (f,path) = tempfile.mkstemp(dir=settings.MAGPIE_DIR + '/../resources/media')
    os.write(f, pml)
    os.close(f)
    traverse = subprocess.Popen([settings.PML_PATH + "/graph/traverse",'-R','-L',path],stdout=subprocess.PIPE)
    dotDesc = traverse.communicate()[0]  
    os.remove(path)
    return (dotDesc,path)
        
def pmlView(request):
    try:
        pmlPath = request.GET.items()[0][1]
        reqType = request.GET.items()[1][1]
    except:
        return HttpResponse("[ERROR] Expecting two arguments.",mimetype='text/html')
    if reqType not in ["graph","viewer","pml","roadmap"]:
        return HttpResponse("[ERROR] Invalid action. Must be graph, viewer, pml, roadmap.",mimetype='text/html')
    if pmlPath.find("../") != -1:
        return HttpResponse("[ERROR] '../' contained in specified file name, relative paths unallowed for security reasons.",mimetype='text/html')
    fullPath = settings.MEDIA_ROOT + pmlPath
    if os.path.isfile(fullPath):
        if reqType == "roadmap":
            roadmap = '<html>\n\n'
            roadmap += xmlToRoadmap(fullPath)
            roadmap += '\n</html>\n'
            return HttpResponse(roadmap,mimetype='text/html')
        pmlDesc = xmlToPml(fullPath)
        if pmlDesc is None:
            return HttpResponse("[ERROR] Could not convert XML to PML.",mimetype='text/html')
        if reqType == "pml":
            return HttpResponse(pmlDesc, mimetype="text/plain")
        dotDescInfo = pmlToDot(pmlDesc)
        if dotDescInfo[0] is None:
            return HttpResponse("[ERROR] Could not convert PML to DOT.",mimetype='text/html')
        graph = pydot.graph_from_dot_data(dotDescInfo[0])
        if reqType == "graph":
            jpg = graph.create_jpg()
            return HttpResponse(jpg, mimetype="image/jpg")
        elif reqType == "viewer":
            mapHtml = '<html>\n<body>\n'
            mapHtml += graph.create_cmapx()
            mapHtml += "\n\n"
            mapHtml += '<img src="../pmlView?path='+ pmlPath +'&type=graph" usemap="#' + os.path.basename(dotDescInfo[1]) + '"/>\n\n'
            mapHtml += '</body>\n</html>\n\n'
            return HttpResponse(mapHtml, mimetype="text/html")            
    else:
        return HttpResponse("[ERROR] File not found.",mimetype='text/html')        
        
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
    summaryClosure = recSummaryClosure(request.user)
    recommends = map(summaryClosure,state.get_recommends())
    return render_to_response('knowledge/saved.html', {
                'recommend_list': recommends,
                'reason_list' : state.get_reasons()
                }, context)

def ask_or_done(request, state):
    context = RequestContext(request)
    questions = state.get_questions()
    summaryClosure = recSummaryClosure(request.user)
    recommends = map(summaryClosure,state.get_recommends())
    reasons = state.get_reasons()
    put_state(request.session, state)
    # check if all done
    if len(questions) == 0:
        return render_to_response(
            'knowledge/done.html', {
                'recommend_list': recommends,
                'reason_list' : reasons
            },
            context)
    # keep going
    return render_to_response(
        'knowledge/ask.html', {
        'question_list': questions,
        'recommend_list': recommends,
        'reason_list': reasons
        },
        context)


def ask(request):
    context = RequestContext(request)
    if request.method == 'POST':
        # user answered some questions
        answers =  get_answers(request.POST.items())
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            profile.save_answers(profile.get_answers() + answers)
        state = get_state(request.session)
        state.next_state(answers)
        rsp = ask_or_done(request, state)
    else:
        # first time
        state = start_state(request.user)
        state.next_state()
        #This is a hack until we figure out a better way to save 
        #progress
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            profile.save_answers([])
        rsp = ask_or_done(request, state)
    return rsp

# save state here if logged in (else keep in cookie)
def done(request):
    context = RequestContext(request)
    #Force redirect to index, instead of redirecting to '/'
    return redirect(index)

    
#Reset saved answers
def reset(request):
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        profile.save_answers([])
    return redirect(index)
