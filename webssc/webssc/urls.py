from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'wowstat.views.wowza'),
    url(r'^listsession/$', 'ssc.views.listsession'),

    (r'^accounts/login/$',  'ssc.views.user_login'),
    (r'^accounts/login/welcome/$',  direct_to_template, {
        'template': 'ssc/welcome.html'
    }),

    (r'^accounts/logout/$', 'ssc.views.user_logout'),
    (r'^accounts/logout/goodbye/$',  direct_to_template, {
        'template': 'ssc/goodbye.html'
    }),
)
