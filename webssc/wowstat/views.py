# -*- coding: utf-8 -*-

import os
#import sqlite3
import psycopg2
import httplib2
import ConfigParser
import xml.etree.ElementTree as etree
from django.template.response import TemplateResponse


PATH = os.path.realpath(os.path.dirname(__file__))

config = ConfigParser.RawConfigParser()
config.read(PATH + '/../ssc_conf.ini')
server_ip = config.get('wowza', 'server_ip')
server_port = config.get('wowza', 'server_port')
login = config.get('wowza', 'login')
password = config.get('wowza', 'password')
postgres_user = config.get('postgresql', 'user')
postgres_pass = config.get('postgresql', 'pass')

translate = {
    'veltonMedium46.stream': 'Поле Металлист. Низкое качество',
    'veltonQuality46.stream': 'Поле Металлист. Высокое качество',
    'veltonMedium47.stream': 'Детская площадка. Низкое качество',
    'veltonQuality47.stream': 'Детская площадка. Высокое качество',
    'veltonMedium48.stream': 'Вид на Металлист. Низкое качество',
    'veltonQuality48.stream': 'Вид на Металлист. Высокое качество',
    'veltonMedium49.stream': 'Пл. свободы. Низкое качество',
    'veltonQuality49.stream': 'Пл. свободы. Высокое качество',
    'veltonMedium50.stream': 'Донецк. Низкое качество',
    'veltonQuality50.stream': 'Донецк. Высокое качество',
    'veltonMedium51.stream': 'Днепропетровск. Низкое качество',
    'veltonQuality51.stream': 'Днепропетровск. Высокое качество',
    'veltonMedium52.stream': 'Одесса. Низкое качество',
    'veltonQuality52.stream': 'Одесса. Высокое качество',
    'veltonMedium53.stream': 'Полтава. Низкое качество',
    'veltonQuality53.stream': 'Полтава. Высокое качество',
    'veltonMedium54.stream': 'Зеркальная струя. Низкое качество',
    'veltonQuality54.stream': 'Зеркальная струя. Высокое качество',
    'veltonMedium55.stream': 'Киев. Низкое качество',
    'veltonQuality55.stream': 'Киев. Высокое качество',
}


def wowza(request):
    """Make a connection to wowza server, retrieve 
       /connectioncounts url and get detailed connections info.
       Then select summary info about last two days connection info.
    """
    h = httplib2.Http()
    h.add_credentials(login, password)

    try:
        root = etree.fromstring(h.request('http://' + server_ip + ':' +
                                server_port + '/connectioncounts/')[1])
    except Exception as e:
        return TemplateResponse(request, 'wowstat/error.html', {'err': str(e)})

    detail = []
    # Find streams info in returned xml.
    for child in (root.find('VHost').find('Application').
                 find('ApplicationInstance').findall('Stream')):
        # Save total session information
        detail.append([child.findall('Name')[0].text,
                       child.findall('SessionsTotal')[0].text])

    for i in detail:  # change stream name (name.stream) to human readable
        if i[0] in translate:
            i[0] = translate[i[0]]

    # Making connection to wowza server.
    ############################################################
    # Sqlite3
    #conn = sqlite3.connect(PATH + '/wowstat.db')
    ############################################################
    # Postgresql
    conn = psycopg2.connect("dbname='test_wowstat' user={0} password={1}"
                            .format(postgres_user, postgres_pass))
    ############################################################
    cur = conn.cursor()
    ############################################################
    # Sqlite3
    #cur.execute('select * from summary order by -id limit 288;')
    ############################################################
    # Postrgesql
    cur.execute('SELECT query_time::time(0), conn_counts FROM summary ORDER BY -id LIMIT 288')
    ############################################################

    summary = []
    for i in reversed(cur.fetchall()):
        summary.append([i[0], i[1]])

    # Fix 'one letter' format in minutes section - temporary for sqlite only.
    #for i, v in enumerate(summary):
    #    if len(v[0].split(':')[1]) == 1:
    #        summary[i] = [v[0].split(':')[0] + ':0' +
    #                      v[0].split(':')[1], v[1]]

    conn.commit()
    cur.close()
    conn.close()

    return TemplateResponse(request, 'wowstat/wowza.html',
                            {'detail': detail, 'current': root[0].text,
                             'summary': summary})
