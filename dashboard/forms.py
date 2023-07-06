from django.db import models
from .models import UploadWellPictureModel,water_quality_model,featuresForm, physical_features_model
from .models import water_usable_model, cultural_model, human_form_model
from django import forms

class UploadWellPictureForm(forms.ModelForm):
    class Meta:
        model = UploadWellPictureModel
        fields = ('picture','name','well_nm','radius','depth','level','village','district','state','pincode', 'lat', 'lng','water_quality','wells_type')

class quality_form(forms.ModelForm):
    class Meta:
        model = water_quality_model
        fields = ('name','state','district','taluka','village','gram_panch', 'water_quality','color','odour','taste', 'ph','turbid','hard','chloride','alkaline','nitrate','fluoride','iron','chlorine','calcium','magnesium','date')

class features_form(forms.ModelForm):
    class Meta:
        model = featuresForm
        fields = ('district','taluka','village','stretchNo','stretchStart','stretchEnd','owner',   'projectIncharge','revisionNo','contactNo','latitude','longitude','date','feature','description')

class physical_features_form(forms.ModelForm):
    class Meta:
        model = physical_features_model
        fields = ('district','taluka','village','stretchNo','stretchStart','stretchEnd','owner',   'projectIncharge','revisionNo','contactNo','latitude','longitude','date','feature','description')

class water_usable_form(forms.ModelForm):
    class Meta:
        model = water_usable_model
        fields = ('district','taluka','village','stretchNo','stretchStart','stretchEnd','owner',   'projectIncharge','revisionNo','contactNo','latitude','longitude','date','feature','description')

class cultural_form(forms.ModelForm):
    class Meta:
        model = cultural_model
        fields = ('district','taluka','village','stretchNo','stretchStart','stretchEnd','owner',   'projectIncharge','revisionNo','contactNo','latitude','longitude','date','feature','description')

class human_form_form(forms.ModelForm):
    class Meta:
        model = human_form_model
        fields = ('district','taluka','village','stretchNo','stretchStart','stretchEnd','owner',   'projectIncharge','revisionNo','contactNo','latitude','longitude','date','feature','description')
