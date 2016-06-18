from django.conf.urls import url,include
from django.contrib.gis import admin


urlpatterns = [
    url(r'^', include('editor.urls')),
    url(r'^tms/', include('shapeEditor.tms.urls')),
    url(r'^admin/', admin.site.urls),
]

# Example:
# (r'^geodjango/', include('geodjango.foo.urls')),
# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
# to INSTALLED_APPS to enable admin documentation:
# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
# Uncomment the next line to enable the admin:

