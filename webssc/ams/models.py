# -*- coding: utf-8 -*-

from django.db import models

import os
import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate


def fetcher(key):
    """
    fetcher(key: str) -> function fetcher
    """
    a = {}
    config = ConfigParser.RawConfigParser()
    config.read(PATH + '/../ssc_conf.ini')
    items = config.items(key)

    a[key] = [item[1] for item in items if item[1] != '']

    return a

PATH = os.path.realpath(os.path.dirname(__file__))
SEND_TO = fetcher('send_to')
SEND_FROM = fetcher('send_from')
SMTP_IP = fetcher('smtp_ip')
SMTP_PORT = fetcher('smtp_port')


class Phone(models.Model):
    number = models.CharField(max_length=20)
  
    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name_plural = "Телефоны"


class Engineer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40, blank=True)
    post = models.CharField(max_length=50, blank=True)
    email = models.EmailField('E-mail', blank=True)
    phone = models.ManyToManyField(Phone, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "Инженеры"


class Publisher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    post = models.CharField(max_length=50, blank=True)
    email = models.EmailField('E-mail', blank=True)
    phone = models.ManyToManyField(Phone, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "Открывают аварии"


class State(models.Model):
    title = models.CharField(max_length=10)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Состояния"


class Step(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    engineer = models.ManyToManyField(Engineer)
    publisher = models.ForeignKey(Publisher)
    publication_datetime = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Этапы"


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    engineer = models.ManyToManyField(Engineer, blank=True)
    step = models.ManyToManyField(Step, blank=True)
    publisher = models.ForeignKey(Publisher)
    publication_datetime = models.DateTimeField(blank=True, null=True)
    starting_datetime = models.DateTimeField(blank=True, null=True)
    closing_datetime = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(State) 

    def __unicode__(self):
        return self.title

    def save(self):
        super(Event, self).save()
        self.send_mail(SMTP_IP, SMTP_PORT, SEND_FROM, {'send_to': ['misokolsky@gmail.com']},
                       self.title, u'авария добавлена или изменена', 'http://sokolskiy.masq.lc/ams/')

    @staticmethod
    def send_mail(smtp_ip, smtp_port, send_from, send_to, event_title, message, link):
        """
        send_mail(smtp_ip: dict, smtp_port: dict, send_from: dict, send_to: dict,
                  user: str, login_name: str, reply: str) -> None
        """
        msg = MIMEMultipart()
        msg['From'] = send_from['send_from'][0]
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'Reply AMS.'
        msg['To'] = COMMASPACE.join(send_to['send_to'])
        msg.attach(MIMEText(event_title.encode('UTF-8')+': '+message.encode('UTF-8')+'\n'+link))

        smtp = smtplib.SMTP(smtp_ip['smtp_ip'][0], int(smtp_port['smtp_port'][0]))
        smtp.sendmail(send_from['send_from'][0], send_to['send_to'], msg.as_string())


    class Meta:
        verbose_name_plural = "Аварии"
