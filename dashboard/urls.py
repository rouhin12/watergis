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
    path('dashboard/watergis', views.watergis, name = 'watergis'),
    path('dashboard/capt_wells', views.capt_wells, name = 'capt_wells'),
    path('dashboard/uploadwellpic', views.uploadwellpic, name='uploadwellpic')
    

]
