from django.conf.urls import patterns, url

urlpatterns = patterns('lazyplant.views',
    url(r'^upload_iot/', 'upload_iot'),
    url(r'^myplant/', 'myplant'),
    url(r'^myplant_vid/', 'myplant_vid'),
    )

