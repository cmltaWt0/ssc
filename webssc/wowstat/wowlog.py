#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import sqlite3
import httplib2
import ConfigParser
import xml.etree.ElementTree as etree

# sqlite3 wowstat.db
# CREATE TABLE summary (id INTEGER, time, counts, PRIMARY KEY(id ASC));

hour = str(time.localtime().tm_hour)
minuts = str(time.localtime().tm_min)

PATH = os.path.realpath(os.path.dirname(__file__))

config = ConfigParser.RawConfigParser()
config.read(PATH + '/../ssc_conf.ini')
server_ip = config.get('wowza', 'server_ip')
server_port = config.get('wowza', 'server_port')
login = config.get('wowza', 'login')
password = config.get('wowza', 'password')

h = httplib2.Http(PATH + '/.cache')
h.add_credentials(login, password)

with open(PATH + '/.cache/xml_log', mode='w') as a_file:
    a_file.write(h.request('http://' + server_ip + ':' + server_port + '/connectioncounts/')[1].decode('utf-8'))

tree = etree.parse(PATH + '/.cache/xml_log')
root = tree.getroot()

conn = sqlite3.connect(PATH + '/wowstat.db')
cur = conn.cursor()
cur.execute("INSERT INTO summary VALUES (null, ?, ?)", (hour+':'+minuts, root[0].text))

conn.commit()
cur.close()
conn.close()

# chmod +x path_to_project/ssc/webssc/wowstat/wowlog.py
# */10 *  * * *   user  path_to_project/ssc/webssc/wowstat/wowlog.py

