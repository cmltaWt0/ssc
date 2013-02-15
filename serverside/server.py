#! /usr/bin/env python2.4
# coding=utf-8

import socket

from modules import FILE_OUT, send_mail, fetcher, write_log, execute, \
    login_test, correction

'''
TCP server with synchronous behaviour. Execute one client at a time.
I is not high load system, so asynchronous is not necessary.

Client <-> Server exchange:
  1. Server <- Client == user:str
      2.1 Server -> Client == 'ok':str if OK
      2.2 Server -> Client == 'User '+user+' is not allowed to delete session.':str otherwise
          2.2.1 Session close
  3. Server <- Client == login_name:str
      4.1 Server -> Client == 'ok':str if OK
      4.2 Server -> Client == 'Incorrect login.':str otherwise('' or ' ')
          4.2.1 Session close
  5. Server <- Client == listSession:str 'del' or 'list' for different command
      6.1 Server -> Client == 'Connection lost' if quit received
      6.2 Server -> Client == result:str correct result
      6.3 Server -> Client == login_name+' Syntax error.':str
'''

try:
    ALLOWED_USER = fetcher('users')['users']
    SEND_TO = fetcher('send_to')
    SEND_FROM = fetcher('send_from')
    SMTP_IP = fetcher('smtp_ip')
    SMTP_PORT = fetcher('smtp_port')
except Exception, failure:
    write_log(FILE_OUT, 'Error: ', 'system', 'Error: ', str(failure))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 0000


def main():
    while True:
        try:
            try:
                client, address = s.accept()
                address = '@' + address[0]
                user = client.recv(32)

                if user in ALLOWED_USER:
                    client.send('ok')  # send confirmation to client
                    login_name = client.recv(64)
                    client.send('ok')
                    listSession = client.recv(8)
                else:
                    client.send('User ' + user + ' is not allowed to delete session.')
                    client.close()
                    #write_log(FILE_OUT, user+address, 'Access', 'Not allowed to delete session.')
                    #send_mail(SEND_TO, user+address, 'Access', 'Not allowed to delete session.')
                    send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                              user + address, 'Access', 'Not allowed to delete session.')
                    continue

            except Exception, failure:
                #write_log(FILE_OUT, 'Socket ' , 'system', 'Error: ', str(failure))
                send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                          'Error', 'system', str(failure))
                continue

            login_name = correction(login_name)

            if login_name == 'QUIT':
                client.send('Connection lost.')
                client.close()
                s.close()
                break

            if login_test(login_name):
                result = execute(login_name, listSession)
                #write_log(FILE_OUT, user+address, login_name, result.rstrip())
                #send_mail(SEND_TO, user+address, login_name, result.rstrip())
                send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                          user + address, login_name, result.rstrip())
                client.send(result.rstrip())
                client.close()
            else:
                #write_log(FILE_OUT, user+address, login_name, 'Syntax error.')
                #send_mail(SEND_TO, user+address, login_name, 'Syntax error.')
                send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                          user + address, login_name, 'Syntax error.')
                client.send(login_name + ' Syntax error.')
                client.close()

        except Exception, failure:
            #write_log(FILE_OUT, user+address, login_name, 'Error: ', str(failure))
            send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                      user + address, login_name, str(failure))


try:
    s.bind((host, port))
    s.listen(5)
except Exception, failure:
    #write_log(FILE_OUT, 'Error ' , 'system', 'Error: ', str(failure))
    send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']}, 'Error', 'system', str(failure))
    raise

if __name__ == '__main__':
    main()
