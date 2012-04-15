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
from utils import OrderedDict

# note sesson is a gui state so
# should not pass to business logic layer
#Unit tested
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

#Unit tested   
def del_state(session):
    try:
      del session['engine']
    except KeyError:
      pass

#Unit tested
def put_state(session, state):
    session['engine'] = state_encode(state) 

#Unit tested
def get_state(session):
    if 'engine' in session:
        slist = session['engine']
    else:
        slist = []
    return state_decode(slist)

#Given an XML file path, turn it into a PML spec
#Unit tested
def xmlToPml(filePath):
    #Redirect XML errors away from stdout so that it doesn't cause a
    #mod_wsgi exception.
    libxml2.registerErrorHandler(lambda ctx,str: None, None)
    libxslt.registerErrorHandler(lambda ctx,str: None, None)
    pmlStyleDoc=libxml2.parseFile(settings.PML_PATH + "/xpml/xpml.xsl")
    style = libxslt.parseStylesheetDoc(pmlStyleDoc)
    try:
        doc = libxml2.parseFile(filePath)
        result = style.applyStylesheet(doc, None)
        return style.saveResultToString(result)
    except (libxml2.parserError, TypeError):
        return None

#Given an XML file path, turn it into a Roadmap document
#Unit tested        
def xmlToRoadmap(filePath):
    libxml2.registerErrorHandler(lambda ctx,str: None, None)
    libxslt.registerErrorHandler(lambda ctx,str: None, None)
    pmlStyleDoc=libxml2.parseFile(settings.PML_PATH + "/xpml/pmldoc.xsl")
    style = libxslt.parseStylesheetDoc(pmlStyleDoc)
    try:
        doc = libxml2.parseFile(filePath)
        result = style.applyStylesheet(doc, None)
        return style.saveResultToString(result)
    except (libxml2.parserError, TypeError):
        return None
    
#Take PML description, turn it into a DOT graph description.
#Unit tested
def pmlToDot(pml):
    if pml is None:
        return None  
    (f,path) = tempfile.mkstemp(dir=settings.MAGPIE_DIR + '/../resources/media')
    os.write(f, pml)
    os.close(f)
    traverse = subprocess.Popen([settings.PML_PATH + "/graph/traverse",'-j','-R','-L',path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = traverse.communicate()   
    dotDesc = output[0]
    #Capture stderr... if there's something here, something has probably gone wrong...
    os.remove(path) 
    if output[1]:
        return None
    return (dotDesc,path)

#One big view that takes a filename, and view type, and gives back 
#either a graph, a viewer for an interactive graph, a roadmap page or a 
#plaintext PML spec. Most of the code is error handling...        
#Unit tested
def pmlView(request):
    try:
        pmlPath = request.GET.items()[0][1]
        reqType = request.GET.items()[1][1]
        if (request.GET.items()[0][0] != "path") or (request.GET.items()[1][0] != "type"):
            return HttpResponse("[ERROR] Invalid GET request.",mimetype='text/html')
    except:
        return HttpResponse("[ERROR] Expecting two arguments.",mimetype='text/html')
    if reqType not in ["graph","viewer","pml","roadmap"]:
        return HttpResponse("[ERROR] Invalid action. Must be graph, viewer, pml, roadmap.",mimetype='text/html')
    if pmlPath.find("../") != -1:
        return HttpResponse("[ERROR] '../' contained in specified file name, relative paths unallowed for security reasons.",mimetype='text/html')
    fullPath = settings.MEDIA_ROOT + pmlPath
    if os.path.isfile(fullPath):
        if reqType == "roadmap":
            roadmapDesc = xmlToRoadmap(fullPath)
            if roadmapDesc is None:
                return HttpResponse("[ERROR] Unable to create roadmap description - file not found, or parse error.",mimetype='text/html')
            roadmap = '<html>\n\n'
            roadmap += roadmapDesc
            roadmap += '\n</html>\n'
            return HttpResponse(roadmap,mimetype='text/html')
        pmlDesc = xmlToPml(fullPath)
        if pmlDesc is None:
            return HttpResponse("[ERROR] Unable to create PML description - file not found, or parse error.",mimetype='text/html')
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

#Unit tested
def index(request):
    context = RequestContext(request)
    if request.method == 'POST':
        del_state(request.session)
        return redirect(ask)
    return render_to_response('knowledge/index.html', context)

#Used when user changes their answers.
#Unit tested
def saved (request):
    answers =  get_answers(request.POST.items())
    #Make blank state, add the backlog of answers, get next state
    state = start_state(request.user)
    state.add_vars(answers,1)
    state.next_state()
    priorQuestions = state.getPriorQuestions(state.get_answers())
    #If logged in, save progress to profile
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        profile.save_answers(answers)
    return ask_or_done(request, state, priorQuestions)

#Unit tested
def ask_or_done(request, state, priorQuestions):
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
                'reason_list' : reasons,
                'priorQuestions' : priorQuestions
            },
            context)
    # keep going
    return render_to_response(
        'knowledge/ask.html', {
        'question_list': questions,
        'recommend_list': recommends,
        'reason_list': reasons,
        'priorQuestions': priorQuestions
        },
        context)

#Unit tested
def ask(request):
    context = RequestContext(request)
    if request.method == 'POST':
        # user answered some questions
        answers =  get_answers(request.POST.items())
        state = get_state(request.session)
        state.next_state(answers)
        priorQuestions = state.getPriorQuestions(state.get_answers())
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            profile.save_answers(state.get_answers())
        return ask_or_done(request, state, priorQuestions)
    else:
        # User clicks Start on Index...
        state = start_state(request.user)
        priorQuestions = None
        #If logged in, grab prior progress and use it to resume.
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            priorAnswers = profile.get_answers()
            state.add_vars(priorAnswers,1)
            priorQuestions = state.getPriorQuestions(profile.get_answers())
        state.next_state()
        return ask_or_done(request, state, priorQuestions)
    
#Reset saved answers
#Unit tested
def reset(request):
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        profile.save_answers([])
    return redirect(index)
