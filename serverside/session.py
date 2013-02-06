#! /usr/bin/env python2.4

import re

from modules import FILE_OUT, send_mail, fetcher, open_file, write_log, clear_file, execute, login_test

"""
This is temporary decision while server is not ready for production.
This app trying to open dinput.txt file in user's home directory and 
parse for login_name's.
"""

try:
    ALLOWED_USER = fetcher('users')['users']
    SEND_TO = fetcher('send_to')
    SEND_FROM = fetcher('send_from')
    SMTP_IP = fetcher('smtp_ip')
    SMTP_PORT = fetcher('smtp_port')
except Exception, failure:
    write_log(FILE_OUT, 'Error: ', 'system', 'Error: ', str(failure))


def main(ALLOWED_USER, SEND_TO):  # For testing
    for user in ALLOWED_USER:
        try:
            file_path = '/export/home/'+user+'/dinput.txt'
            login_name_list = open_file(file_path)
            if login_name_list is not None:  # If open_file not return None
                for login_name in login_name_list:
                    login_name = re.sub(' +', ' ', login_name) 
                    if login_test(login_name): 
                        result = execute(login_name)
                        write_log(FILE_OUT, user, login_name, result.rstrip())
                        send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, SEND_TO, user, login_name, result.rstrip())
                    else:
                        write_log(FILE_OUT, user, login_name, 'Possible syntax or semantic error.')
                        send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, SEND_TO, user, login_name,
                                  'Possible syntax or semantic error.')
                clear_file(file_path)
        except Exception, failure:
            write_log(FILE_OUT, user, 'system', 'Error: ', str(failure))
            send_mail(SMTP_IP, SMTP_PORT,  SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                      user, 'system', str(failure))


if __name__ == '__main__':
    main(ALLOWED_USER, SEND_TO)
