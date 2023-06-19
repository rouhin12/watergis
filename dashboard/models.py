from django.contrib.gis.db import models
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    state_name = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.state_name}, {self.district_name}"



class Layers(models.Model):
    TITLE_CHOICES = [
        ('natural_features', 'natural_features'),
        ('man_made_water_related_features', 'man_made_water_related_features'),
        ('man_made_other_features', 'man_made_other_features'),
        ('population', 'population'),
        ('antyodaya', 'antyodaya'),
        
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

    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True, default=None)
    title_id = models.CharField(max_length=100,choices=TITLE_CHOICES)
    sub_title = models.CharField(max_length=100,choices=SUB_TITLE)
    display_checkbox_name = models.CharField(max_length=100)
    value=models.CharField(max_length=100)
    method=models.CharField(max_length=100)
    features = models.ForeignKey(Features, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.sub_title}, {self.display_checkbox_name}"
    
class water_quality_model(models.Model):
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
    ph = models.IntegerField(max_length=5,blank=True, null=True)
    turbid = models.IntegerField(max_length=5,blank=True, null=True)
    hard = models.IntegerField(max_length=15,blank=True, null=True)
    chloride = models.IntegerField(max_length=15,blank=True, null=True)
    alkaline = models.IntegerField(max_length=15,blank=True, null=True)
    nitrate = models.FloatField(max_length=15,blank=True, null=True)
    fluoride = models.FloatField(max_length=15,blank=True, null=True)
    iron = models.FloatField(max_length=15,blank=True, null=True)
    chlorine = models.FloatField(max_length=15,blank=True, null=True)
    calcium = models.FloatField(max_length=15,blank=True, null=True)
    magnesium = models.FloatField(max_length=15,blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name
class links(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100)
    def __str__(self):
        return self.title