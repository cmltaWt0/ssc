# -*- coding: utf-8 -*
from django import forms

ACTIVE_CHOICES = (
    ('Открыто', 'Открытые'),
    ('Закрыто', 'Закрытые'),
)

DISPLAYED_CHOICES = (
    ('5', '5'),
    ('10', '10'),
    ('20', '20'),
    ('30', '30'),
)

class EventForm(forms.Form):
    choise = forms.CharField(required=False, label='Тип аварии', max_length=7,
                widget=forms.Select(choices=ACTIVE_CHOICES))
    displayed = forms.CharField(required=False, label='Показывать', max_length=2,
                widget=forms.Select(choices=DISPLAYED_CHOICES))
