from django.conf.urls.defaults import *


urlpatterns = patterns('mediator.views',
    (r'^$', 'list'),
    (r'^query$', 'query'),
    (r'^search/$', 'search'),
    (r'^mkdir/$', 'mkdir'),
    (r'^upload/$', 'upload'),
)

