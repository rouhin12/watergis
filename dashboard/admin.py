from django.contrib import admin
from .models import UploadWellPictureModel
from .models import Features
from .models import Layers
from .models import water_quality_model
from .models import links

admin.site.register(UploadWellPictureModel)
# Register your models here.
admin.site.register(Features)

admin.site.register(Layers)
admin.site.register(water_quality_model)
admin.site.register(links)