# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from ams.models import Event, Engineer, Phone, Step
from ams.forms import EventForm

@login_required
def default(request):
    """
    Show default page ams's app.
    """
    if request.method == 'GET':
        form = EventForm(request.GET)
        try: 
            choise = request.GET['choise']
            displayed = request.GET['displayed']
        except:
            choise = 'Открыто'
            displayed = 5 
        if choise and displayed:
            event = Event.objects.filter(state__title__contains=choise).order_by('publication_datetime')[0:int(displayed)]
    return TemplateResponse(request, 'ams/default_ams.html', locals())

@login_required
def detail(request, id):
    """
    Showing event details
    """
    event = Event.objects.filter(id=id)
    step = Step.objects.filter(event=event)
    engineer = Engineer.objects.filter(event=event)
    return TemplateResponse(request, 'ams/detail_ams.html', locals())

@login_required
def detail_engineer(request, id):
    """
    Showing engineer details
    """
    engineer = Engineer.objects.filter(id=id)
    phone = Phone.objects.filter(engineer=engineer)
    return TemplateResponse(request, 'ams/detail_engineer_ams.html', locals())

@login_required
def detail_step(request, id):
    """
    Showing event details
    """
    step = Step.objects.filter(id=id)
    engineer = Engineer.objects.filter(step=step)
    return TemplateResponse(request, 'ams/detail_step.html', locals())
