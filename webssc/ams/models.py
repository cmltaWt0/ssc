# -*- coding: utf-8 -*-
from django.db import models

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

    class Meta:
        verbose_name_plural = "Аварии"
