from datetime import datetime
from django.db import models
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from language.models import *
from launchie.models import Project
cachedir = "~/.cache/ "
from launchpadlib.launchpad import Launchpad
from pprint import pprint

def home(request):
    languages = Language.objects.all()
    
    return render_to_response(
            'homepage.html',
            {'languages': languages,},
            context_instance=RequestContext(request)
        )

def search(request):
    launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)
    
    if not "lang" in request.GET:
        return redirect('/')
        
    language = request.GET['lang']
    query = request.GET['q'] if ("q" in request.GET and request.GET['q'] != "[e.g. Django]") else ''
    
    projects_response = launchpad.projects.search(text=(query if query else None))
        
    projects = []
    
    for pr in projects_response:
        proj = []
        try:
            lang = pr.programming_language.lower()
        except Exception as e:
            lang = pr.programming_language
            
        if (lang == language.lower() or not language) and (pr.active == True):
            proj.append(pr.name)
            proj.append(pr.web_link)
            summary = pr.summary.replace("\n", " ")
            proj.append(summary)
            if not proj in projects:
                projects.append(proj)
        
    """
    for project in projects :
        print project.name
        try:
            lang = project.programming_language.lower()
        except Exception as e:
            lang = project.programming_language
        if lang == language.lower() or not language:
            if project.summary:
                s = project.summary.replace("\n", " ")
                s = s[:80-(len(project.name) + 6)].strip() + "..."
            else:
                pass
    """
    
    return render_to_response(
            'searchpage.html',
            {'projects': projects,},
            context_instance=RequestContext(request)
        )

def dump(request):
    launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)
    projects = launchpad.projects.search(text=None)
    
    for project in projects:
        try:
            lang = project.programming_language.lower()
        except Exception as e:
            lang = project.programming_language
        s = ' '
        if project.summary:
            s = project.summary.replace("\n", " ")
            s = s[:80-(len(project.name) + 6)].strip() + "..."
        else:
            pass    
            
        pl = project.programming_language if project.programming_language else ''
        
        proj = Project(name = project.name, summary = s, 
            active = project.active, owner = project.owner,
            logo = '', web_link = project.web_link, 
            programming_language = pl,
            updated_at = datetime.now())
        proj.save()
