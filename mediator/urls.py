from django.conf.urls.defaults import *


urlpatterns = patterns('mediator.views',
    url(r'^$', 'list',  name='list'),
    (r'^query$', 'query'),
    (r'^search/$', 'search'),
    (r'^mkdir/$', 'mkdir'),
    (r'^upload/$', 'upload'),
)

