#! /usr/bin/env python2.7

# TODO ADD login feature
# TODO ADD Database intergation (sqlite3) - display last action with related user
# TODO Reading config file once at start, not at any request.

import socket
#import sqlite3
import ConfigParser

from flask import Flask, render_template, request


city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA']
point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11', 'K12', 'K13', 'K14', 'K45', 'K20', 'X00']
#DATABASE = '/tmp/webclient.db'
#SECRET_KEY = 'develop key'

app = Flask(__name__)


def fetcher(key):
    """
    fetcher(key: str) -> function fetcher
    """
    a = {}
    config = ConfigParser.RawConfigParser()
    config.read('/home/maksim/PycharmProjects/ssc/webclient/conf.ini')
    items = config.items(key)

    a[key] = [item[1] for item in items if item[1] != '']

    return a


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/help/")
def help():
    return render_template('help.html')


@app.route('/listsession/', methods=['GET', 'POST'])
def listsession():
    if request.method == 'POST' and 'login_del' in request.form and request.form['submit'] == 'Delete':
        login_name = request.form['login_del']
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = fetcher('server_ip')['server_ip'][0]
        port = int(fetcher('server_port')['server_port'][0])

        try:
            s.connect((host, port))
        except Exception as e:
            return render_template('form.html', city=city, point=point, result=str(e))

        else:
            user = fetcher('user')['user'][0]
            s.send(user)
            response = s.recv(64)

            if response == 'ok':
                s.send(login_name)
                response = s.recv(24)
                if response == 'ok':
                    s.send('del')
                    msg = s.recv(1024)
                    return render_template('form.html', city=city, point=point, result=msg.split('\n'))
                else:
                    return render_template('form.html', city=city, point=point, result=response)

            else:
                return render_template('form.html', city=city, point=point, result=response)
        finally:
            s.close()

    elif request.method == 'POST' and 'login_name' in request.form:

        if request.form['type'] == 'raw' and request.form['login_name'] != '':

            login_name = request.form['login_name']
        elif request.form['type'] == 'comp':
            try:
                opt1 = str(int(request.form['opt1']))
                opt2 = str(int(request.form['opt2']))
                opt3 = '0' + str(int(request.form['opt3']))
                opt4 = '0' + str(int(request.form['opt4']))
                opt5 = str(int(request.form['opt5']))
                opt6 = str(int(request.form['opt6']))
                opt7 = str(int(request.form['opt7']))
            except ValueError:
                return render_template('form.html', city=city, point=point, result=['Incorrect input.'])

            login_name = request.form['city'] + '-' + request.form['point'] + ' PON ' + \
                         opt1 + '/' + opt2 + '/' + opt3 + '/' + opt4 + ':' + opt5 + '.' + opt6 + '.' + opt7
        else:
            return render_template('form.html', city=city, point=point, result=['Incorrect input.'])

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = fetcher('server_ip')['server_ip'][0]
        port = int(fetcher('server_port')['server_port'][0])

        try:
            s.connect((host, port))
        except Exception as e:
            return render_template('form.html', city=city, point=point, result=str(e))

        else:
            user = fetcher('user')['user'][0]
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
                        return render_template('form.html', city=city, point=point,
                                               result=msg.split('\n'), login_name=login_name)
                    else:
                        return render_template('deleter.html', result=msg.split('\n'), login_name=login_name)
                else:
                    return render_template('form.html', city=city, point=point, result=response)

            else:
                return render_template('form.html', city=city, point=point, result=response)
        finally:
            s.close()
    else:
        return render_template('form.html', city=city, point=point, result='')


if __name__ == "__main__":
    app.run(host='192.168.53.24', port=80, debug=True)
