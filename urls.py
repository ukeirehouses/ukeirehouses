from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
                       (r'^', include('ukeirehouses.urls')),
                       ('^_ah/warmup$', 'djangoappengine.views.warmup'),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       (r'^profiles/', include('profiles.urls')),


#                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
#                       (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),set


                       ('^$', 'django.views.generic.simple.direct_to_template',
                        {'template': 'home.html'}),
)
