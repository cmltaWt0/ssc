from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
import socket
import ConfigParser
import os
import re


PATH = os.path.realpath(os.path.dirname(__file__))

city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA', 'MARIUPOL']
point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11',
         'K12', 'K13', 'K14', 'K45', 'K20', 'X00']


config = ConfigParser.RawConfigParser()
config.read(PATH + '/../ssc_conf.ini')
host = config.get('server', 'server_ip')
port = int(config.get('server', 'server_port'))


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
    login_part = login_name.split(' ')
    if (login_part[0].split('-')[0] not in city or login_part[0].split('-')[1]
        not in point):
        return False
    elif login_part[1] != 'PON' and login_part[1] != 'eth':
        return False
    elif not login_part[2][-1].isdigit():
        return False
    else:
        return True


def correction(login_name):
    """
    correction(login_name: str) -> str
    """
    login_name = login_name.strip()
    login_name = re.sub(' +', ' ', login_name)
    login_name = login_name.upper()
    login_name = re.sub('ETH', 'eth', login_name)

    return login_name


def make_request(user, login_name, method='list'):
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
        response = 'Error: ' + login_name + ' Syntax error.'

    return response


def socket_request(request):
    """Common code for making similar logic for http_request and ajax_request.

    DRY similar code between simple HTTP and Ajax requests to this function.
    Using make_request function for making request to socket server.
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

        result = make_request(user, login_name, method='del')
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
                opt1 = str(int(request.POST['opt1']))
                opt2 = str(int(request.POST['opt2']))
                if len(str(int(request.POST['opt3']))) == 1:
                    opt3 = '0' + str(int(request.POST['opt3']))
                else:
                    opt3 = str(int(request.POST['opt3']))
                opt4 = '0' + str(int(request.POST['opt4']))
                opt5 = str(int(request.POST['opt5']))
                opt6 = str(int(request.POST['opt6']))
                opt7 = str(int(request.POST['opt7']))
            except ValueError:
                result = ['Incorrect input.']
                return {'result': result, 'login_name': login_name, 'delete': delete}

            login_name = (request.POST['city'] + '-' + request.POST['point'] +
                          ' PON ' + opt1 + '/' + opt2 + '/' + opt3 + '/' +
                          opt4 + ':' + opt5 + '.' + opt6 + '.' + opt7)
        else:
            result = ['Incorrect input.']
            return {'result': result, 'login_name': login_name, 'delete': delete}

        result = make_request(user, login_name)

        if 'No sessions' in result or 'Err' in result:
            # Negative respone
            result = result.split('\n')
            return {'result': result, 'login_name': login_name, 'delete': delete}

        else:
            # Positive response
            msg_result = {}
            sec = 1

            # Separating different sessions
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

            delete = True
            result = msg_result
            return {'result': result, 'login_name': login_name, 'delete': delete}

    # GET method received - showing clear form
    else:
        return {'result': result, 'login_name': login_name, 'delete': delete}



def ajax_socket_request(request):
    """Temporary for ajax testing.
    """
    user = request.user.username
    login_name = request.POST['login_name']

    result = (make_request(user, login_name) if login_name != ''
                                             else ['Incorrect input.'])

    return {'result': result, 'login_name': login_name}


def xml_request(request):
    """Making request to SSC API.

    Construct HTTP  request to SSC including appropriate XML data included.
    Returning response as a dictionary.
    """
    return {'result': ['Not implemented yet.']}


@csrf_protect
@login_required(login_url='/ssc/accounts/login/')
def simple_http_handler(request, xml):
    """Simple HTTP request handler.

    Render template with response as a dictionary.
    """
    response = xml_request(request) if xml else socket_request(request)

    # Adding choices for select input in from.html
    #######################################
    response['city'] = city
    response['point'] = point
    #######################################
    return TemplateResponse(request, 'ssc/form.html', response)


@csrf_protect
@login_required(login_url='/ssc/accounts/login/')
def ajax_http_handler(request, xml):
    """Ajax HTTP request handler.

    """
    response = xml_request(request) if xml else ajax_socket_request(request)

    return HttpResponse(response['result'])
 
