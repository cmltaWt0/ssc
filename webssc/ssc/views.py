from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
import socket
import ConfigParser
import os


PATH = os.path.realpath(os.path.dirname(__file__))

city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA', 'MARIUPOL']
point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11', 'K12', 'K13', 'K14', 'K45', 'K20', 'X00']


config = ConfigParser.RawConfigParser()
config.read(PATH + '/../ssc_conf.ini')
host = config.get('server', 'server_ip')
port = int(config.get('server', 'server_port'))


def user_login(request):
    """
    Login func
    """
    if request.user.is_authenticated():
         return TemplateResponse(request, 'ssc/already_logged.html')
    else:
         return views.login(request, template_name='ssc/login.html')

def user_logout(request):
    """
    Logout func
    """
    if request.user.is_authenticated():
        return views.logout(request, next_page=reverse('ssc:goodbye'))
    else:
        return TemplateResponse(request, 'ssc/not_logged.html')


@login_required(login_url='/listsession/accounts/login/')
def listsession(request):
    # Delete(second) part of request
    if request.method == 'POST' and 'login_del' in request.POST and request.POST['submit'] == 'Delete':
        login_name = request.POST['login_del']
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((host, port))
        except Exception as e:
            return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': str(e)})

        else:
            user = request.user.username
            s.send(user)
            response = s.recv(64)

            if response == 'ok':
                s.send(login_name)
                response = s.recv(24)
                if response == 'ok':
                    s.send('del')
                    msg = s.recv(1024)
                    return TemplateResponse(request, 'ssc/form.html',
                                            {'city': city, 'point': point, 'result': msg.split('\n'),
                                             'login_name': login_name})
                else:
                    return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point,
                                                                       'result': response})

            else:
                return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': response})
        finally:
            s.close()

    # List(first) part of request - mandatory part
    elif request.method == 'POST' and 'login_name' in request.POST:
        # If user choise first option - write SSID in text mode
        if request.POST['type'] == 'raw' and request.POST['login_name'] != '':
            login_name = request.POST['login_name']
        # If user choise second option - to compound SSID
        elif request.POST['type'] == 'comp':
            try:
                opt1 = str(int(request.POST['opt1']))
                opt2 = str(int(request.POST['opt2']))
                opt3 = '0' + str(int(request.POST['opt3']))
                opt4 = '0' + str(int(request.POST['opt4']))
                opt5 = str(int(request.POST['opt5']))
                opt6 = str(int(request.POST['opt6']))
                opt7 = str(int(request.POST['opt7']))
            except ValueError:
                return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point,
                                                                   'result': ['Incorrect input.']})

            login_name = request.POST['city'] + '-' + request.POST['point'] + ' PON ' + \
                         opt1 + '/' + opt2 + '/' + opt3 + '/' + opt4 + ':' + opt5 + '.' + opt6 + '.' + opt7
        else:
            return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point,
                                                               'result': ['Incorrect input.']})

        # Make connection to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((host, port))
        except Exception as e:
            return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': str(e)})

        else:
            user = request.user.username
            s.send(user)
            response = s.recv(64)

            if response == 'ok':
                s.send(login_name)
                response = s.recv(24)
                if response == 'ok':
                    s.send('list')
                    msg = s.recv(2048)
                    if msg == 'No sessions were found which matched the search criteria.' or \
                                    'Syntax' in msg.split() or msg == 'Connection lost.':
                        # When received a negative response from server after handshake
                        return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point,
                                               'result': msg.split('\n'), 'login_name': login_name})
                    else:
                        # Positive response
                        msg_result = {}
                        sec = 1

                        for base_part in msg.split('SessionParcel'):  # Separating different sessions
                            if len(base_part) == 0: continue
                            msg_result['Session ' + str(sec)] = []
                            for i in base_part.split('\n'):           # Separating session parameters
                                if '=' in i and ('Timestamp' in i or 'UserIpAddr' in i or 'Domain' in i):
                                    msg_result['Session ' + str(sec)].append(i)
                            sec += 1

                        return TemplateResponse(request, 'ssc/deleter.html', {'result': msg_result,
                                                                              'login_name': login_name})
                else:
                    # Login-name test is not passed on server
                    return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point,
                                                                       'result': response})

            else:
                # User is not approved
                return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': response})
        finally:
            s.close()

    # GET method received - showing clear form
    else:
        return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point})
