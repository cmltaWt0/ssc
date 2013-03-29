import re
import subprocess
import ConfigParser
from datetime import datetime

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate


FILE_OUT = '/var/adm/sub-session_delete.log'


def send_mail(smtp_ip, smtp_port, send_from, send_to, user, login_name, reply):
    """
    send_mail(smtp_ip: dict, smtp_port: dict, send_from: dict, send_to: dict,
              user: str, login_name: str, reply: str) -> None
    """
    msg = MIMEMultipart()
    msg['From'] = send_from['send_from'][0]
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Reply from sub-session_deleter.'
    msg['To'] = COMMASPACE.join(send_to['send_to'])
    msg.attach(MIMEText(user+': '+login_name+': '+reply))

    smtp = smtplib.SMTP(smtp_ip['smtp_ip'][0], int(smtp_port['smtp_port'][0]))
    smtp.sendmail(send_from['send_from'][0], send_to['send_to'], msg.as_string())


def fetcher(key):
    """
    fetcher(key: str) -> function fetcher
    """
    a = {}
    config = ConfigParser.RawConfigParser()
    config.read('/opt/ssc/conf.ini')
    items = config.items(key)

    a[key] = [item[1] for item in items if item[1] != '']

    return a


def open_file(file_path):
    """
    open_file(file_path: str) -> result: list

    Open input and return list of login_names.

    open_file(file_path) input -> String: path to input file'.
    Returns String : list of login_names.
    File format:
        LOGINNAME1
        LOGINNAME2
        LOGINNAME3
        ...
    """
    result = []
    #if user deleted input file
    try:
        f = open(file_path, 'rb')
    except:
        return
    try:
        for line in f:
            line = line.strip()
            if line != '':
                result.append(line)
    finally:
        f.close()

    return result


def write_log(file_path, user, login_name, text, err=''):
    """
    write_log(file_path: str, user: str, login_name: str, text: str, err='': str) -> None
    """
    ##LOG FORMAT: {date: user: username(SSID): result}
    f = open(file_path, 'a')
    try:
        now = str(datetime.now()).split()
        f.write(now[0]+'-'+now[1].split('.')[0] + ': ' + user + ': ' + login_name + ': ' + text + err + '\n')
    finally:
        f.close()


def clear_file(file_path):
    """
    clear_file(file_path: str) -> None
    """
    f = open(file_path, 'wb')
    f.close()


def execute(login_name, listSession='del'):
    """
    execute(login_name: str, listSession=False) -> result: str

    Execution delSession utility of SSC server if list is 'del'.
    listSession otherwise.

    execute(login_name, listSession) input -> String: sort of 'KHARKIV K13-1-2-3:34:1.1'.
    Returns String -> result
    """
    if listSession == 'del':
        proc = subprocess.Popen('/WideSpan/utilities/RMSCmd/delSessions -rms 0 -nointeractive -l "' + login_name + '"',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)
        result = proc.communicate()[0]
    else:
        proc = subprocess.Popen('/WideSpan/utilities/RMSCmd/listSessions -rms 0 -l "' + login_name + '"',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)
        result = proc.communicate()[0]

    return result


def login_test(login_name):
    """
    login_test(login_name: str) -> bool
    """
    city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA']
    point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11', 'K12', 'K13', 'K14', 'K20', 'K45', 'X00']

    login_part = login_name.split(' ')
    if login_part[0].split('-')[0] not in city or login_part[0].split('-')[1] not in point:
        return False
    elif login_part[1] != 'PON':
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

    return login_name
