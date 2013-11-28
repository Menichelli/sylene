from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'sylene.views.home', name='home'),
     url(r'^viewer/', 'sylene.views.viewer', name='viewer'),
     url(r'^login/', 'sylene.views.login_', name='login'),
     url(r'^logout/', 'sylene.views.logout_', name='logout'),
     url(r'^userpanel/add_user', 'sylene.views.add_user', name='add_user'),
     url(r'^userpanel/create_user', 'sylene.views.create_user', name='create_user'),
     url(r'^userpanel/add_tech_survey', 'sylene.views.add_tech_survey', name='add_tech_survey'),
     url(r'^userpanel/conf_tech_survey', 'sylene.views.conf_tech_survey', name='conf_tech_survey'),
     url(r'^userpanel/', 'sylene.views.userpanel', name='userpanel'),
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^nyi/', 'sylene.views.nyi', name='nyi'),
)
