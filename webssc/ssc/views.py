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


PATH = os.path.realpath(os.path.dirname(__file__))

city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA', 'MARIUPOL']
point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11',
         'K12', 'K13', 'K14', 'K45', 'K20', 'X00']

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


def login_test(login_name):
    """
    login_test(login_name: str) -> bool
    """
    correct = True
    login_part = login_name.split(' ')

    if login_name == '' or len(login_part) != 3:
        correct = False
    else:
        last_part = re.sub('[/:.]', '*', login_part[2]).split('*')
        try:
            if (len(last_part) != 7 or
                0 in map(int, last_part) or
                login_part[0].split('-')[0] not in city or
                login_part[0].split('-')[1] not in point or
                (login_part[1] != 'PON' and login_part[1] != 'eth')):
                correct = False
        except ValueError:
                correct = False

    return correct


def correction(login_name):
    """
    correction(login_name: str) -> str
    """
    login_name = login_name.strip()
    login_name = re.sub(' +', ' ', login_name)
    login_name = login_name.upper()
    login_name = re.sub('ETH', 'eth', login_name)

    return login_name


def socket_request(user, login_name, method='list'):
    """
    Make raw socket connection to server.
    """
    login_name = correction(login_name)
    if login_test(login_name) or login_name == 'QUIT':
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
    else:
        response = 'Error: ' + login_name + ' Incorrect input/Syntax error.'

    return re.sub(' +', ' ', response)


def xml_request(login_name):
    """Making request to SSC API.

    Construct HTTP  request to SSC including appropriate XML data included.
    Returning response as a string.
    """
    login_name = correction(login_name)
    msg_result = ['Something goes wrong...']
    delete = False

    if login_test(login_name):
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

    else:
        msg_result = [re.sub(' +', ' ', 'Error: ' + login_name + ' Incorrect input/Syntax error.')]

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


def http_handler(request):
    """Common code for making similar logic for http_request and ajax_request.

    DRY similar code between simple HTTP and Ajax requests to this function.
    Using socket_request function for making request to socket server.
    Returning response as a dictionary.
    """

    delete = False
    result = False
    login_name = False
    user = request.user.username
    # Deleting session(second) part of request
    if (request.method == 'POST' and 'login_del' in request.POST and
                request.POST['submit'] == 'Delete'):

        login_name = request.POST['login_del']

        result = socket_request(user, login_name, method='del')
        result = result.split('\n')
        return {'result': result, 'login_name': login_name, 'delete': delete}

    # Listening session(first) part of request - mandatory part
    elif request.method == 'POST' and 'login_name' in request.POST:
        # If user choice first option - write SSID in text mode
        if request.POST['type'] == 'raw' and request.POST['login_name'] != '':
            login_name = request.POST['login_name']
        # If user choice second option - to compound SSID
        elif request.POST['type'] == 'comp':
            try:
                opt1 = str(int(request.POST.get('opt1', False)))
                opt2 = str(int(request.POST.get('opt2', False)))
                if len(str(int(request.POST.get('opt3', False)))) == 1:
                    opt3 = '0' + str(int(request.POST.get('opt3', False)))
                else:
                    opt3 = str(int(request.POST.get('opt3', False)))
                opt4 = '0' + str(int(request.POST.get('opt4', False)))
                opt5 = str(int(request.POST.get('opt5', False)))
                opt6 = str(int(request.POST.get('opt6', False)))
                opt7 = str(int(request.POST.get('opt7', False)))
                if request.POST.get('city', False) and request.POST.get('point', False):
                    city, point = request.POST['city'], request.POST['point']
                else:
                    raise ValueError

            except ValueError:
                result = ['Error: Incorrect input/Syntax error.']
                return {'result': result, 'login_name': login_name, 'delete': delete}

            login_name = (city + '-' + point + ' PON ' + opt1 + '/' + opt2 + '/' + opt3 + '/' +
                          opt4 + ':' + opt5 + '.' + opt6 + '.' + opt7)
        else:
            result = ['Error: Incorrect input/Syntax error.']
            return {'result': result, 'login_name': login_name, 'delete': delete}

        result, delete = make_human_readable(socket_request(user, login_name))
        return {'result': result, 'login_name': login_name, 'delete': delete}

    # GET method received - showing clear form
    else:
        return {'result': result, 'login_name': login_name, 'delete': delete}


@csrf_protect
@login_required(login_url='/ssc/accounts/login/')
def dispatcher(request):
    """
    Dispatcher for ajax and simple http request.
    """
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        user = request.user.username
        login_name = request.POST['login_name'] if request.POST.get('login_name', False) else ''
        method = request.POST['method'] if request.POST.get('method', False) else 'list'

        result, delete = make_human_readable(socket_request(user, login_name, method))
        if '[Errno 111] Connection refused' in result:
            result, delete = xml_request(login_name)
        return HttpResponse(json.dumps((result, delete)), content_type="application/json")
    else:
        response = http_handler(request)

        # Adding choices for select input in from.html
        #######################################
        response['city'] = city
        response['point'] = point
        #######################################
        return TemplateResponse(request, 'ssc/form.html', response)
