from datetime import datetime
from django.db import models
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from search.models import *
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
    if not "lang" in request.GET:
        return redirect('/')
        
    launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)
    projects = []

    language = request.GET['lang']
    query = request.GET['q'] if ("q" in request.GET and request.GET['q'] != "[e.g. Django]") else ''
    
    projects_response = launchpad.projects.search(text=(query if query else None))
    
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
                
    l = Language.objects.get(slug=language)
    search_query = Query(
        language = l,
        text = query,
        searched_at = datetime.now(),
        from_ip = request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else ''
    )
    search_query.save()
    
    return render_to_response(
            'searchpage.html',
            {'projects': projects,},
            context_instance=RequestContext(request)
        )
