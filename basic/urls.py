from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'basic.views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests$', 'basic.views.requests', name='first-requests'),
    url(r'^edit$', 'basic.views.edit', name='edit-profile'),
    url(r'^save$', 'basic.views.save', name='save-profile'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', 
    		{'template_name': 'login.html'}, name="login"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
	+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

