from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'xms.views.default', name='default'),

    url(r'^accounts/login/$', 'xms.views.user_login', name='login'),
    url(r'^accounts/login/welcome/$', TemplateView.as_view(template_name='xms/welcome.html'), name='welcome'),

    url(r'^accounts/logout/$', 'xms.views.user_logout', name='logout'),
    url(r'^accounts/logout/goodbye/$', TemplateView.as_view(template_name='xms/goodbye.html'), name='goodbye'),
)
