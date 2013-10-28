# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.contrib.comments.signals import comment_was_posted
from django.dispatch import receiver

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
    description = models.TextField()
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
    description = models.TextField()
    engineer = models.ManyToManyField(Engineer, blank=True)
    step = models.ManyToManyField(Step, blank=True)
    publisher = models.ForeignKey(Publisher)
    publication_datetime = models.DateTimeField(blank=True, null=True)
    starting_datetime = models.DateTimeField(blank=True, null=True)
    closing_datetime = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(State) 

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Аварии"


@receiver(post_save, sender=Event, dispatch_uid="EventSaveDispatch")
def send_mail(sender, **kwargs):
        """
        send_mail(smtp_ip: dict, smtp_port: dict, send_from: dict, send_to: dict,
                  user: str, login_name: str, reply: str) -> None
        """
        msg = MIMEMultipart()
        msg['From'] = SEND_FROM['send_from'][0]
        msg['Date'] = formatdate(localtime=True)

        if 'instance' in kwargs:
            instance = kwargs['instance']
            text = instance.title
            msg['Subject'] = u'Авария создана или изменена.'
        elif 'comment' in kwargs:
            text = kwargs['comment'].comment
            msg['Subject'] = u'Добавлен новый комментарий.'

        msg['To'] = COMMASPACE.join(SEND_TO['send_to'])
        msg.attach(MIMEText(text.encode('UTF-8')+'\n'+'http://sokolskiy.masq.lc/ams/'))

        smtp = smtplib.SMTP(SMTP_IP['smtp_ip'][0], int(SMTP_PORT['smtp_port'][0]))
        smtp.sendmail(SEND_FROM['send_from'][0], SEND_TO['send_to'], msg.as_string())

comment_was_posted.connect(send_mail, dispatch_uid='CommentPostDispatch')