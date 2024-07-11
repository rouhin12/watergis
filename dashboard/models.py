from django.contrib.gis.db import models
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext as _

class UploadWellPictureModel(models.Model):
    picture = models.ImageField( upload_to='WellPics/', blank=True, null=True, default='WellPics/noImage.jpg')
    name = models.CharField(max_length=100, blank=True, null=True)
    well_nm = models.CharField(max_length=100, blank=True, null=True)
    radius = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=8, blank=True, null=True)
    lat = models.CharField(max_length=15)
    lng = models.CharField(max_length=15)
    water_quality = models.CharField(max_length=40)
    wells_type = models.CharField(max_length=40)
    def save(self, *args, **kwargs):
        if not self.id:
            self.picture = self.compressImage(self.picture)
        super(UploadWellPictureModel, self).save(*args, **kwargs)
    def compressImage(self,picture):
        imageTemproary = Image.open(picture)
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproary = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        picture = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return picture
    class Meta:
       managed = True
       db_table = 'upload_well'


class Features(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.BooleanField()
    district = models.BooleanField()
    natural_features=models.BooleanField()
    drainage = models.BooleanField()
    rivers = models.BooleanField()
    ground_water_recharge_priority= models.BooleanField()
    villages_near_river= models.BooleanField()
    man_made_water_related_features= models.BooleanField()
    water_shed_boundaries= models.BooleanField()
    man_made_other_features= models.BooleanField()
    population= models.BooleanField()
    census = models.BooleanField()
    geographical_hierarchy= models.BooleanField()
    antodaya = models.BooleanField()
    contours=models.BooleanField()
    rainfall=models.BooleanField()
    gw_prospects=models.BooleanField()
    state_name = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.state_name}, {self.district_name}"
    class Meta:
       managed = True
       db_table = 'dashboard_features'



class Layers(models.Model):
    TITLE_CHOICES = [
        ('natural_features', 'natural_features'),
        ('man_made_water_related_features', 'man_made_water_related_features'),
        ('man_made_other_features', 'man_made_other_features'),
        ('population', 'population'),
        ('antyodaya', 'antyodaya'),
        ('rainfall', 'rainfall'),
        ('layers', 'layers'),
        
        
    ]
    
    SUB_TITLE=[
        ('drainage','drainage'),
        ('rivers','rivers'),
        ('ground_water_recharge_priority','ground_water_recharge_priority'),
        ('villages_near_river','villages_near_river'),
        ('watershed_boundaries','watershed_boundaries'),
        ('census','census'),
        ('geographical_hierarchy','geographical_hierarchy'),
        ('antodaya','antodaya'),
        ('basins','basins'),
        ('contours','contours'),
        ('rainfall','rainfall'),
        ('layers','layers'),

    ]
    FUNCTION_CHOICES = (
    ('putWMS1', 'putWMS1'),
    ('putWMS2', 'putWMS2'),
    ('putWMS', 'putWMS'),
    )

    METHOD_CHOICES = (
    ('getBoundary(this)', 'getBoundary(this)'),
    ('showAntodaya2(this)', 'showAntodaya2(this)'),
    ('showAntodaya(this)', 'showAntodaya(this)'),
    ('showContours(this)', 'showContours(this)'),
    ('showDrainage(this)', 'showDrainage(this)'),
    )
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True, default=None)
    title_id = models.CharField(max_length=100,choices=TITLE_CHOICES)
    sub_title = models.CharField(max_length=100,choices=SUB_TITLE)
    display_checkbox_name = models.CharField(max_length=100)
    value=models.CharField(max_length=100)
    method=models.CharField(max_length=100,choices=METHOD_CHOICES)
    latlong=models.CharField(max_length=100)
    function = models.CharField(max_length=100, choices=FUNCTION_CHOICES)
    zoomlevel=models.CharField(max_length=100)
    cql=models.CharField(max_length=100)
    features = models.ForeignKey(Features, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.sub_title}, {self.display_checkbox_name}"
    class Meta:
       managed = True
       db_table = 'layers'
    
    
class WaterQualityModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    taluka = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    gram_panch = models.CharField(max_length=100, blank=True, null=True)
    water_quality = models.CharField(max_length=100, null=True)
    color=models.CharField(max_length=100, null=True)
    odour=models.CharField(max_length=100, null=True)
    taste=models.CharField(max_length=100, null=True)
    ph = models.IntegerField(blank=True, null=True)
    turbid = models.IntegerField(blank=True, null=True)
    hard =models.IntegerField(blank=True, null=True)
    chloride = models.IntegerField(blank=True, null=True)
    alkaline = models.IntegerField(blank=True, null=True)
    nitrate = models.FloatField(blank=True, null=True)
    fluoride = models.FloatField(blank=True, null=True)
    iron = models.FloatField(blank=True, null=True)
    chlorine = models.FloatField(blank=True, null=True)
    calcium = models.FloatField(blank=True, null=True)
    magnesium = models.FloatField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name
    class Meta:
       managed = True
       db_table = 'water_quality_model'
class links(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class featuresForm(models.Model):
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    stretchNo = models.CharField(max_length=100)
    stretchStart = models.DateField(blank=True, null=True)
    stretchEnd = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=100)
    projectIncharge = models.CharField(max_length=100)
    revisionNo = models.CharField(max_length=100)
    contactNo = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    feature = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.district_name
    
    
class physical_features_model(models.Model):
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    stretchNo = models.CharField(max_length=100)
    stretchStart = models.DateField(blank=True, null=True)
    stretchEnd = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=100)
    projectIncharge = models.CharField(max_length=100)
    revisionNo = models.CharField(max_length=100)
    contactNo = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    feature = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.district_name
    
class water_usable_model(models.Model):
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    stretchNo = models.CharField(max_length=100)
    stretchStart = models.DateField(blank=True, null=True)
    stretchEnd = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=100)
    projectIncharge = models.CharField(max_length=100)
    revisionNo = models.CharField(max_length=100)
    contactNo = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    feature = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.district_name

class cultural_model(models.Model):
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    stretchNo = models.CharField(max_length=100)
    stretchStart = models.DateField(blank=True, null=True)
    stretchEnd = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=100)
    projectIncharge = models.CharField(max_length=100)
    revisionNo = models.CharField(max_length=100)
    contactNo = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    feature = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.district_name

class human_form_model(models.Model):
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    stretchNo = models.CharField(max_length=100)
    stretchStart = models.DateField(blank=True, null=True)
    stretchEnd = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=100)
    projectIncharge = models.CharField(max_length=100)
    revisionNo = models.CharField(max_length=100)
    contactNo = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    feature = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.district_name
    
    
class MahaRiversFromOsmV116June23(models.Model):
    geom = models.GeometryField(srid=4326)
    fid = models.IntegerField(blank=True, null=True)
    full_id = models.CharField(max_length=254, blank=True, null=True)
    osm_id = models.CharField(max_length=254, blank=True, null=True)
    osm_type = models.CharField(max_length=254, blank=True, null=True)
    waterway = models.CharField(max_length=254, blank=True, null=True)
    name_mr = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maha_rivers_from_osm_v1_16june23'

class MahaDemoV2126April24(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    geom = models.GeometryField(srid=4326)  # Example for MultiPolygon

    fid_1 = models.CharField(max_length=254, blank=True, null=True)
    fid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dist_name = models.CharField(max_length=254, blank=True, null=True)
    area_name = models.CharField(max_length=254, blank=True, null=True)
    dist_lgd = models.CharField(max_length=254, blank=True, null=True)
    cen_2011 = models.CharField(max_length=254, blank=True, null=True)
    dist_2001 = models.CharField(max_length=254, blank=True, null=True)
    taluka_201 = models.CharField(max_length=254, blank=True, null=True)
    ward = models.CharField(max_length=254, blank=True, null=True)
    tru = models.CharField(max_length=254, blank=True, null=True)
    no_hh = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    p_06 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    m_06 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    f_06 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    p_sc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    m_sc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    f_sc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    p_st = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    m_st = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    f_st = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    p_lit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    m_lit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    f_lit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    p_ill = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    m_ill = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    f_ill = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_work_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_work_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_work_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mainwork_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mainwork_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mainwork_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_cl_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_cl_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_cl_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_al_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_al_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_al_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_hh_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_hh_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_hh_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_ot_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_ot_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    main_ot_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_cl_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_cl_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_cl_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_al_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_al_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_al_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_hh_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_hh_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_hh_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_ot_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_ot_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_ot_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_3 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_cl_3_field = models.DecimalField(db_column='marg_cl_3_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_cl_1 = models.DecimalField(db_column='marg_cl__1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_cl_2 = models.DecimalField(db_column='marg_cl__2', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_al_3_field = models.DecimalField(db_column='marg_al_3_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_al_1 = models.DecimalField(db_column='marg_al__1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_al_2 = models.DecimalField(db_column='marg_al__2', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_hh_3_field = models.DecimalField(db_column='marg_hh_3_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_hh_1 = models.DecimalField(db_column='marg_hh__1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_hh_2 = models.DecimalField(db_column='marg_hh__2', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_ot_3_field = models.DecimalField(db_column='marg_ot_3_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_ot_1 = models.DecimalField(db_column='marg_ot__1', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_ot_2 = models.DecimalField(db_column='marg_ot__2', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    margwork_0 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_4 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    margwork_5 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    marg_cl_0_field = models.DecimalField(db_column='marg_cl_0_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_cl_3 = models.DecimalField(db_column='marg_cl__3', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_cl_4 = models.DecimalField(db_column='marg_cl__4', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_al_0_field = models.DecimalField(db_column='marg_al_0_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_al_3 = models.DecimalField(db_column='marg_al__3', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_al_4 = models.DecimalField(db_column='marg_al__4', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_hh_0_field = models.DecimalField(db_column='marg_hh_0_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_hh_3 = models.DecimalField(db_column='marg_hh__3', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_hh_4 = models.DecimalField(db_column='marg_hh__4', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    marg_ot_0_field = models.DecimalField(db_column='marg_ot_0_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    marg_ot_3 = models.DecimalField(db_column='marg_ot__3', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    non_work_p = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    non_work_m = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    non_work_f = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    taluka_nam = models.CharField(max_length=254, blank=True, null=True)
    dist_2011 = models.CharField(max_length=254, blank=True, null=True)
    marg_ot_5 = models.DecimalField(db_column='marg_ot__5', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    layer = models.CharField(max_length=254, blank=True, null=True)
    path = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maha_demo_v21_26april24'
    
