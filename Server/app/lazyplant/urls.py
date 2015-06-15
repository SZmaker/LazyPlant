from django.conf.urls import patterns, url

urlpatterns = patterns('lazyplant.views',
    url(r'^upload_iot/', 'upload_iot'),
    )

