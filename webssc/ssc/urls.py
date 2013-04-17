from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'ssc.views.listsession'),

    url(r'^accounts/login/$', 'ssc.views.user_login'),
    url(r'^accounts/login/welcome/$', direct_to_template, {
        'template': 'ssc/welcome.html'
    }),

    url(r'^accounts/logout/$', 'ssc.views.user_logout'),
    url(r'^accounts/logout/goodbye/$', direct_to_template, {
        'template': 'ssc/goodbye.html'
    }),

)