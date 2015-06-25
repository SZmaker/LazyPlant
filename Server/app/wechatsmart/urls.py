from django.conf.urls import patterns, url

urlpatterns = patterns('wechatsmart.views',
    url(r'^$', 'smart_entry'),
    )
