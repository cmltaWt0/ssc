from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', namespace='admindocs')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^$', TemplateView.as_view(template_name='base.html'), name='index'),

    url(r'^wowstat/', include('wowstat.urls', namespace='wowstat')),
    url(r'^ssc/', include('ssc.urls', namespace='ssc')),
    url(r'^ams/', include('ams.urls', namespace='ams')),
    url(r'^xms/', include('xms.urls', namespace='xms')),

)

