from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'ams.views.default'),
    (r'^event/(?P<id>\d{1,3})/$', 'ams.views.detail'),
    (r'^engineer/(?P<id>\d{1,3})/$', 'ams.views.detail_engineer'),
    (r'^step/(?P<id>\d{1,3})/$', 'ams.views.detail_step'),
)
