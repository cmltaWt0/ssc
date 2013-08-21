from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'ssc.views.simple_http_handler', {'xml': False}, name='http'),
    url(r'^xml/$', 'ssc.views.simple_http_handler', {'xml': True}, name='http_xml')

    url(r'^ajax/$', 'ssc.views.ajax_http_handler', {'xml': False}, name='ajax'),
    url(r'^ajax/xml/$', 'ssc.views.ajax_http_handler', {'xml': True}, name='ajax_xml'),

    url(r'^accounts/login/$', 'ssc.views.user_login', name='login'),
    url(r'^accounts/login/welcome/$', TemplateView.as_view(template_name='ssc/welcome.html'), name='welcome'),

    url(r'^accounts/logout/$', 'ssc.views.user_logout', name='logout'),
    url(r'^accounts/logout/goodbye/$', TemplateView.as_view(template_name='ssc/goodbye.html'), name='goodbye'),

)
