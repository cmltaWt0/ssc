from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
import socket
import ConfigParser
import json
import os
import re

import urllib2
import xml.etree.ElementTree as ET

from .forms import SSCForm, MASKForm


PATH = os.path.realpath(os.path.dirname(__file__))

config = ConfigParser.RawConfigParser()
config.read(PATH + '/../ssc_conf.ini')
host = config.get('server', 'server_ip')
port = int(config.get('server', 'server_port'))
ssc_url = config.get('ssc', 'url')
ssc_login = config.get('ssc', 'login')
ssc_pass = config.get('ssc', 'pass')


def user_login(request):
    """
    Login function.
    """
    if request.user.is_authenticated():
        return TemplateResponse(request, 'ssc/already_logged.html')
    else:
        return views.login(request, template_name='ssc/login.html')


def user_logout(request):
    """
    Logout function.
    """
    if request.user.is_authenticated():
        return views.logout(request, next_page=reverse('ssc:goodbye'))
    else:
        return TemplateResponse(request, 'ssc/not_logged.html')


def socket_request(user, login_name, method='list'):
    """
    Make raw socket connection to server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
    except Exception as e:
        response = str(e)

    else:
        s.send(user)
        response = s.recv(64)
        if response == 'ok':
            s.send(login_name)
            response = s.recv(24)
            if response == 'ok':
                s.send(method)
                response = s.recv(2048)
    finally:
        s.close()

    return re.sub(' +', ' ', response)


def xml_request(login_name):
    """Making request to SSC API.

    Construct HTTP  request to SSC including appropriate XML data included.
    Returning response as a string.
    """
    msg_result = ['Caramba...']
    delete = False

    root = ET.parse(PATH + '/getStatus.xml').getroot()
    root.set('principal', ssc_login)
    root.set('credentials', ssc_pass)
    for i in root.iter():
        if i.tag == 'login-name':
            i.text = login_name

    data = ET.tostring(root)

    request = urllib2.Request(url=ssc_url, data=data,
                              headers={'Content-Type': 'application/xml'})
    response = urllib2.urlopen(request).read()
    response_xml = ET.fromstring(response)

    for i in response_xml.iter():
        if i.tag == 'result':
            # Separating different sessions
            msg_result = {}
            sec = 1
            delete = True
            for session in i.findall('operational-status'):
                msg_result['Session ' + str(sec)] = []
                for tag in session:
                    msg_result['Session ' + str(sec)].append(tag.tag+'='+tag.text)
                sec += 1

        elif i.tag == 'error':
            msg_result = [i.find('message').text]

    return msg_result, delete


def make_human_readable(result):
    """
    Make long result string human readable.
    Return dict where different session info in separate list.
    """
    if 'No sessions' in result or 'Err' in result or 'deleted.' in result:
        # Negative response
        delete = False
        msg_result = result.split('\n')
    else:
        # Separating different sessions
        msg_result = {}
        sec = 1
        delete = True

        for base_part in result.split('SessionParcel'):
            if len(base_part) == 0:
                continue
            msg_result['Session ' + str(sec)] = []
            # Separating session parameters
            for i in base_part.split('\n'):
                if '=' in i and \
                        ('Timestamp' in i or 'UserIpAddr' in i
                         or 'Domain' in i or 'NASPort' in i):
                    msg_result['Session ' + str(sec)].append(i)
            sec += 1

    return msg_result, delete

'''
def form_handler(request):
    """
    Pull the login name from form.
    """
    login_name = ['Error: Incorrect input/Syntax error.']  # Default value
    if request.POST['type'] == 'raw' and request.POST['login_name'] != '':
        login_name = request.POST['login_name']
    elif request.POST['type'] == 'comp':
        try:
            opt1 = str(int(request.POST.get('opt1', False)))
            opt2 = str(int(request.POST.get('opt2', False)))
            if len(str(int(request.POST.get('opt3', False)))) == 1:
                opt3 = '0' + str(int(request.POST.get('opt3', False)))
            else:
                opt3 = str(int(request.POST.get('opt3', False)))
            if len(str(int(request.POST.get('opt4', False)))) == 1:
                opt4 = '0' + str(int(request.POST.get('opt4', False)))
            else:
                opt4 = str(int(request.POST.get('opt4', False)))
            opt5 = str(int(request.POST.get('opt5', False)))
            opt6 = str(int(request.POST.get('opt6', False)))
            opt7 = str(int(request.POST.get('opt7', False)))
            if request.POST.get('city', False) and request.POST.get('point', False):
                city, point = request.POST['city'], request.POST['point']
            else:
                raise ValueError
        except ValueError:
            pass

        else:
            login_name = (city + '-' + point + ' PON ' + opt1 + '/' + opt2 + '/' + opt3 + '/' +
                          opt4 + ':' + opt5 + '.' + opt6 + '.' + opt7)
    return login_name
'''

def http_handler(request):
    """
    Generic form handler.
    """
    delete = False
    result = False
    user = request.user.username

    if request.method == 'POST':
        form = SSCForm(request.POST)

        if form.is_valid():
            login_name = form.cleaned_data['login_name']
            method = request.POST['submit']

            if method == 'list' or method == 'del':
                result, delete = make_human_readable(socket_request(user, login_name, method))
    else:
        form = SSCForm()

    return {'result': result, 'delete': delete, 'form': form}


@csrf_protect
@login_required(login_url='/ssc/accounts/login/')
def dispatcher(request):
    """
    Dispatcher for ajax and simple http request.
    """
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        user = request.user.username
        form = SSCForm(request.POST)
        method = request.POST['submit']

        if form.is_valid():
            login_name = form.cleaned_data['login_name']

            if method == 'list' or method == 'del':
                result, delete = make_human_readable(socket_request(user, login_name, method))
                if '[Errno 111] Connection refused' in result:
                    result, delete = xml_request(login_name)
            else:
                result, delete = 'Caramba...', False
        else:
            result, delete = dict(form.errors.items())['login_name'], False
        return HttpResponse(json.dumps((result, delete)), content_type="application/json")
    else:
        response = http_handler(request)
        return TemplateResponse(request, 'ssc/form.html', response)


@csrf_protect
@login_required(login_url='/ssc/accounts/login/')
def mask(request):
    """
    Delete all session in selected POINT.
    """
    user = request.user.username
    result = []
    login_mask = []

    if request.method == 'POST':
        form = MASKForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['city_field']
            point = form.cleaned_data['point_field']
            for i in range(1, 9):
                for j in range(1, 5):
                    for k in range(1, 65):
                        login_mask.append(city+'-'+point+' PON 1/1/0'+str(i)+
                                          '/0'+str(j)+':'+str(k)+'.1.1')

        for i in login_mask:
            #res = i + ' -> ' + socket_request(user, i, 'del')
            res = i + ' -> ' + 'No sessions were found which matched the search criteria.'
            result.append(res)
    else:
        form = MASKForm()

    response = {'result': result, 'form': form}

    return TemplateResponse(request, 'ssc/mask.html', response)
