from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
import socket
import ConfigParser

city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA']
point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11', 'K12', 'K13', 'K14', 'K45', 'K20', 'X00']


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
        return views.logout(request, next_page='/accounts/logout/goodbye/')
    else:
        return TemplateResponse(request, 'ssc/not_logged.html')



def fetcher(key):
    """
    fetcher(key: str) -> function fetcher
    """
    a = {}
    config = ConfigParser.RawConfigParser()
    config.read('/home/maksim/PycharmProjects/ssc/webssc/conf.ini')
    items = config.items(key)

    a[key] = [item[1] for item in items if item[1] != '']

    return a


@login_required
def listsession(request):
    if request.method == 'POST' and 'login_del' in request.POST and request.POST['submit'] == 'Delete':
        login_name = request.POST['login_del']
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = fetcher('server_ip')['server_ip'][0]
        port = int(fetcher('server_port')['server_port'][0])

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
                    return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': msg.split('\n')})
                else:
                    return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': response})

            else:
                return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': response})
        finally:
            s.close()

    elif request.method == 'POST' and 'login_name' in request.POST:

        if request.POST['type'] == 'raw' and request.POST['login_name'] != '':

            login_name = request.POST['login_name']
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
                return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': ['Incorrect input.']})

            login_name = request.POST['city'] + '-' + request.POST['point'] + ' PON ' + \
                         opt1 + '/' + opt2 + '/' + opt3 + '/' + opt4 + ':' + opt5 + '.' + opt6 + '.' + opt7
        else:
            return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': ['Incorrect input.']})

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = fetcher('server_ip')['server_ip'][0]
        port = int(fetcher('server_port')['server_port'][0])

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
                    msg = s.recv(1024)
                    if msg == 'No sessions were found which matched the search criteria.' or \
                                    'Syntax' in msg.split() or msg == 'Connection lost.':
                        return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point,
                                               'result': msg.split('\n'), 'login_name': login_name})
                    else:
                        return TemplateResponse(request, 'ssc/deleter.html', {'result': msg.split('\n'), 'login_name': login_name})
                else:
                    return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': response})

            else:
                return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': response})
        finally:
            s.close()
    else:
        return TemplateResponse(request, 'ssc/form.html', {'city': city, 'point': point, 'result': ''})
