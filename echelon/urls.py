from django.conf.urls.defaults import *

urlpatterns = patterns('echelon.views',
    ('^$', 'changelog'),
)
