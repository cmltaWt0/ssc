from django.conf.urls import patterns, include, url

from django.conf.urls.i18n import i18n_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

#=this made for correct delete translation(simple_translation package)
admin.site.root_path = ''
#===

urlpatterns = i18n_patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls', namespace='admindocs')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^$', TemplateView.as_view(template_name='base.html'), name='index'),

    url(r'^wowstat/', include('wowstat.urls', namespace='wowstat')),
    url(r'^ssc/', include('ssc.urls', namespace='ssc')),
    url(r'^ams/', include('ams.urls', namespace='ams')),
    url(r'^tvdb/', include('tvdb.urls', namespace='tvdb')),
)

