from django.conf.urls import url
from . import views


urlpatterns = [
   url(r'^editor/$', views.list_shapefiles),
   url(r'^import$', views.import_shapefile),
]

