from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'ams.views.default', name='default'),
    url(r'^event/(?P<id>\d{1,3})/$', 'ams.views.detail', name='detail'),
    url(r'^engineer/(?P<id>\d{1,3})/$', 'ams.views.detail_engineer', name='engineer'),
    url(r'^step/(?P<id>\d{1,3})/$', 'ams.views.detail_step', name='step'),

    url(r'^accounts/login/$', 'ams.views.user_login', name='login'),
    url(r'^accounts/login/welcome/$', TemplateView.as_view(template_name='ams/welcome.html'), name='welcome'),

    url(r'^accounts/logout/$', 'ams.views.user_logout', name='logout'),
    url(r'^accounts/logout/goodbye/$', TemplateView.as_view(template_name='ams/goodbye.html'), name='goodbye'),
)
