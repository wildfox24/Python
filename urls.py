from django.conf.urls.defaults import *
#from wwwrsb.views import current_datetime, hours_ahead


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('views',
    # Example:
    # (r'^wwwrsb/', include('wwwrsb.foo.urls')),
    (r'^time/index.html$', 'current_datetime'),
    (r'^time/plus/(\d{1,2}).html$', 'hours_ahead'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('users.views',
    (r'^adduser/$', 'add_user'),
    (r'^edituser/(?P<userID>\d{1,2})/$', 'edit_user'),
    (r'^deleteuser/(?P<userID>\d{1,2})/$', 'delete_user'),
)
