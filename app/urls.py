from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'', include('main.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r"^payments/", include("payments.urls")),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
