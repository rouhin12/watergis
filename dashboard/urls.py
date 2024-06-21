from django.urls import path
# from django.conf.urls import url

from django.contrib import admin
from django.urls import path ,include

from . import views

# from rest_framework import routers

# router = routers.AuthRouter()

urlpatterns = [
    path('', views.HomePage, name = 'homepage'),
    path('dashboard/', views.Dash, name = 'dash'),
    path('dashboard/fgis', views.map, name = 'map'),
    path('dashboard/about', views.about, name = 'about'),
    path('dashboard/watergis', views.watergis_new, name = 'watergis'),
    path('dashboard/watergis2', views.watergis_new2, name = 'watergis2'),
    path('dashboard/watergis_old', views.watergis, name = 'watergis_old'),
    path('dashboard/watergis/waterquality', views.water_quality_form, name = 'waterquality'),
    path('dashboard/watergis/feature', views.feature, name = 'feature'),
    path('set-language/', views.set_language, name='set_language'),
    path('dashboard/watergis/physical_feature', views.physical_feature, name = 'physical_feature'),
    path('dashboard/watergis/water_usable', views.water_usable, name = 'water_usable'),
    path('dashboard/watergis/human_form', views.human_form, name = 'human_form'),
    path('dashboard/watergis/cultural', views.cultural, name = 'cultural'),
    path('dashboard/watergis/district', views.district_view, name = 'district_view'),
    path('dashboard/capt_wells', views.capt_wells, name = 'capt_wells'),
    path('dashboard/uploadwellpic', views.uploadwellpic, name='uploadwellpic'),
    path('dashboard/resources', views.static_files_view, name='resources'),
    path('dashboard/water_related_forms', views.water_related_forms, name='water_related_forms'),
    path('nearestquery',views.nearestquery,name='nearestquery'),
    path('get_layer/', views.get_layer, name='get_layer'),
    # path('get_villages_near_river/', views.get_villages_near_river, name='get_villages_near_river'),
    path('intersecting_villages/', views.intersecting_villages, name='intersecting_villages'),

]
    


