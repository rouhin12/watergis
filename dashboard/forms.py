from django.db import models
from .models import UploadWellPictureModel,water_quality_model
from django import forms

class UploadWellPictureForm(forms.ModelForm):
    class Meta:
        model = UploadWellPictureModel
        fields = ('picture','name','well_nm','radius','depth','level','village','district','state','pincode', 'lat', 'lng','water_quality','wells_type')

class quality_form(forms.ModelForm):
    class Meta:
        model = water_quality_model
        fields = ('name','state','district','taluka','village','gram_panch', 'water_quality','color','odour','taste', 'ph','turbid','hard','chloride','alkaline','nitrate','fluoride','iron','chlorine','calcium','magnesium','date')