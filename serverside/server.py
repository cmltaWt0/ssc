#! /usr/bin/env python2.4
# coding=utf-8

import re
import socket

from modules import FILE_OUT, send_mail, fetcher, write_log, execute, login_test

'''
TCP server with synchronous behaviour. Execute one client at a time.
I is not high load system, so asynchronous is not necessary.
'''

# TODO move check for empty ('' or ' ' -> space) login_name from qtclint and webclient to server!!!!!!!!! very important

try:
    ALLOWED_USER = fetcher('users')['users']
    SEND_TO = fetcher('send_to')
    SEND_FROM = fetcher('send_from')
    SMTP_IP = fetcher('smtp_ip')
    SMTP_PORT = fetcher('smtp_port')
except Exception, failure:
    write_log(FILE_OUT, 'Error: ', 'system', 'Error: ', str(failure))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Create a socket object
host = '172.16.0.1'                                    # Get local machine name
port = 000000                                               # Reserve a port for your service.


def main():
  while True:
      try:
          try:
              client, address = s.accept()      # Establish connection with client.
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
                  send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                            user+address, 'Access', 'Not allowed to delete session.')
                  continue

          except Exception, failure:
              #write_log(FILE_OUT, 'Socket ' , 'system', 'Error: ', str(failure))
              send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                        'Error', 'system', str(failure))
              continue

          login_name = login_name.strip()  # TODO Unificate correction with session.py
          login_name = re.sub(' +', ' ', login_name)
          login_name = login_name.upper()

          if login_name == 'QUIT':
              client.send('Connection lost.')
              client.close()
              s.close()
              break

          if login_test(login_name):
              result = execute(login_name, listSession)
              #write_log(FILE_OUT, user+address, login_name, result.rstrip())
              #send_mail(SEND_TO, user+address, login_name, result.rstrip())
              send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                        user+address, login_name, result.rstrip())
              client.send(result.rstrip())
              client.close()
          else:
              #write_log(FILE_OUT, user+address, login_name, 'Syntax error.')
              #send_mail(SEND_TO, user+address, login_name, 'Syntax error.')
              send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                        user+address, login_name, 'Syntax error.')
              client.send(login_name + ' Syntax error.')
              client.close()

      except Exception, failure:
          #write_log(FILE_OUT, user+address, login_name, 'Error: ', str(failure))
          send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                    user+address, login_name, str(failure))

try:
    s.bind((host, port))
    s.listen(5)
except Exception, failure:
    #write_log(FILE_OUT, 'Error ' , 'system', 'Error: ', str(failure))
    send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']}, 'Error', 'system', str(failure))
    raise


if __name__ == '__main__':
    main()
