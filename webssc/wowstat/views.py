import httplib2
import ConfigParser
import xml.etree.ElementTree as etree
from django.template.response import TemplateResponse


config = ConfigParser.RawConfigParser()
config.read('/home/maksim/PycharmProjects/ssc/webssc/conf.ini')
login = config.get('wowza', 'login')
password = config.get('wowza', 'password')

def wowza(request):
    h = httplib2.Http('/home/maksim/PycharmProjects/ssc/wowstat/.cache')
    h.add_credentials(login, password)

    with open('/home/maksim/PycharmProjects/ssc/wowstat/.cache/xml', mode='w') as a_file:
        a_file.write(h.request('http://85.90.192.233:8086/connectioncounts/')[1].decode('utf-8'))

    tree = etree.parse('/home/maksim/PycharmProjects/ssc/wowstat/.cache/xml')
    root = tree.getroot()

    detail = []
    for child in root.find('VHost').find('Application').find('ApplicationInstance').findall('Stream'):
        detail.append([child.findall('Name')[0].text, child.findall('SessionsTotal')[0].text])

    #if day == ' ': day = str(time.localtime().tm_mday)
    #if mon == ' ': mon = str(time.localtime().tm_mon)
    #if year == ' ': year = str(time.localtime().tm_year)
    #test = []
    #with open('/home/maksim/scripts/wowza/'+day+'.'+mon+'.'+year+'-wowza.log', mode='r') as a_file:
    #    list = a_file.read().split('|')
    #    for i in list:
    #      tmp = i.split('-')
    #      test.append(tmp)
    #    test.pop()
    #title = day+'.'+mon+'.'+year

    #conn_string = "host='localhost' port='19992' dbname='wowza' user='postgres' password='kiwi_mx_strm13Dax'"
    #conn = psycopg2.connect(conn_string)

    #cur = conn.cursor()
    #cur.execute('select * from summary order by -id limit 288;')

    #summary = []
    #for i in reversed(cur.fetchall()):
    #    summary.append([i[1], i[2]])

    #conn.commit()
    #cur.close()
    #conn.close()

    return TemplateResponse(request, 'wowstat/wowza.html', {'detail': detail})