# -*- coding: utf-8 -*-
from django.contrib.auth import views
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import Event, Engineer, Phone, Step
from .forms import EventForm
from .forms import ACTIVE_CHOICES


def user_login(request):
    """
    Login func
    """
    if request.user.is_authenticated():
        return TemplateResponse(request, 'ams/already_logged.html')
    else:
        return views.login(request, template_name='ams/login.html')


def user_logout(request):
    """
    Logout func
    """
    if request.user.is_authenticated():
        return views.logout(request, next_page=reverse('ams:goodbye'))
    else:
        return TemplateResponse(request, 'ams/not_logged.html')


@login_required(login_url='/ams/accounts/login/')
def default(request):
    """
    Show default AMS page.
    """
    if request.method == 'GET':
        form = EventForm(request.GET)

        choice = request.GET.get('choice')
        if (choice is None or len(choice) == 0 or
            choice not in [i[0].decode('utf-8') for i in ACTIVE_CHOICES]):

            choice = 'Открыто'

        try:
            displayed = int(request.GET.get('displayed'))
        except (ValueError, TypeError):
            displayed = 5

        if choice and displayed:
            event = (Event.objects.filter(state__title__contains=choice)
                     .order_by('-publication_datetime')[0:displayed])
            count = len(Event.objects.filter(state__title__contains=choice))
    return TemplateResponse(request, 'ams/default_ams.html', locals())


@login_required(login_url='/ams/accounts/login/')
def detail(request, id):
    """
    Showing event details
    """
    event = Event.objects.filter(id=id)
    step = Step.objects.filter(event=event)
    engineer = Engineer.objects.filter(event=event)
    return TemplateResponse(request, 'ams/detail_ams.html', locals())


@login_required(login_url='/ams/accounts/login/')
def detail_engineer(request, id):
    """
    Showing engineer details
    """
    engineer = Engineer.objects.filter(id=id)
    phone = Phone.objects.filter(engineer=engineer)
    return TemplateResponse(request, 'ams/detail_engineer_ams.html', locals())


@login_required(login_url='/ams/accounts/login/')
def detail_step(request, id):
    """
    Showing step details
    """
    step = Step.objects.filter(id=id)
    engineer = Engineer.objects.filter(step=step)
    return TemplateResponse(request, 'ams/detail_step.html', locals())
