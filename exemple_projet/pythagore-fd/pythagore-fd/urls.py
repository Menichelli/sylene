from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'pythagore.views.home', name='home'),
     
     url(r'^cat/$', 'pythagore.views.catalogue'),
     url(r'^cat/(?P<cat_id>\d+)/$', 'pythagore.views.cat_detail'),
     url(r'^formation/(?P<formation_id>\d+)/$', 'pythagore.views.formation_detail'),
     url(r'^panier/$', 'pythagore.views.panier_view'),
     url(r'^panier/valider/$', 'pythagore.views.valider_panier'),
     url(r'^panier/vider/$', 'pythagore.views.vider_panier'),
     url(r'^commander/(?P<formation_id>\d+)/$', 'pythagore.views.commander'),

     url(r'^register/$', 'pythagore.views.register_form'),
     url(r'^register/validate/$', 'pythagore.views.register_validate'),
     url(r'^login/$', 'pythagore.views.login_'),
     url(r'^logout/$', 'pythagore.views.logout_'),
     url(r'^admin/', include(admin.site.urls)),
)
