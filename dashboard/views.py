from django.shortcuts import render,redirect
from .models import UploadWellPictureModel
from .models import Features
from .models import Layers
from .models import water_quality_model
from .models import links
from django.http import HttpResponse
# from .models import 
from django.contrib import messages
import re,base64,time
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.gis.geos import Point
from .forms import UploadWellPictureForm
from .forms import quality_form, features_form, physical_features_form
from .forms import human_form_form, cultural_form, water_usable_form
from django.http import JsonResponse
from wagtail.documents.models import Document
from wagtail.images.models import Image
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

import os

def HomePage(request):
    return render(request, "HomePage.html")

def Dash(request):
    return render(request, "dashboard/dash.html")

def map(request):
    return render(request, "dashboard/map.html") 

def feature(request):
    return render(request, "dashboard/feature.html") 

def watergis_new(request):
    user_district = request.GET.get('district')
    wells = UploadWellPictureModel.objects.all()
    wellcount = UploadWellPictureModel.objects.count()
    # Query the Features model to get the relevant district
    features = Features.objects.filter(district_name=user_district)

    # Query the Layers model to get the layers related to the district
    layers = Layers.objects.filter(features__district_name=user_district)

    context = {'wells': wells,'wellcount':wellcount,'features': features, 'layers': layers}
    return render(request,'dashboard/watergis.html',context)

def nearestquery(request):
    return render(request,'dashboard/components/nearestquery.html')


def watergis_new2(request):
    user_district = request.GET.get('district')
    wells = UploadWellPictureModel.objects.all()
    wellcount = UploadWellPictureModel.objects.count()
    # Query the Features model to get the relevant district
    features = Features.objects.filter(district_name=user_district)

    # Query the Layers model to get the layers related to the district
    layers = Layers.objects.filter(features__district_name=user_district)
    Alllayers = Layers.objects.all()

    context = {'wells': wells,'wellcount':wellcount,'features': features, 'layers': layers,'alllayers':Alllayers}
    return render(request,'dashboard/watergis2.html',context)

def watergis(request):
    # user_district = request.GET.get('district')
    wells = UploadWellPictureModel.objects.all()
    wellcount = UploadWellPictureModel.objects.count()
    # Query the Features model to get the relevant district
    # features = Features.objects.filter(district_name=user_district)

    # # Query the Layers model to get the layers related to the district
    # layers = Layers.objects.filter(features__district_name=user_district)

    context = {'wells': wells,'wellcount':wellcount}
    return render(request,'dashboard/watergis_backup.html',context)

def about(request):
    return render(request,'dashboard/about.html')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def capt_wells(request):
    form = UploadWellPictureForm()
    global datauri
    # if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        datauri = request.POST['picture']
    
    # if request.method == 'POST' and not request.is_ajax():
    if request.method == 'POST' and not request.META.get('HTTP_X_REQUESTED_WITH'):
        form = UploadWellPictureForm(request.POST, request.FILES)
        form.save(commit=False)
        name = request.POST.get('name')
        well_nm = request.POST.get('well_nm')
        radius = request.POST.get('radius')
        depth = request.POST.get('depth')
        level = request.POST.get('level')
        village = request.POST.get('village')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        water_quality=request.POST.get('water_quality')
        wells_type=request.POST.get('wells_type')
        try:
            imgstr = re.search(r'base64,(.*)', datauri).group(1)
            data = ContentFile(base64.b64decode(imgstr))
            myfile = "WellPics/profile-"+time.strftime("%Y%m%d-%H%M%S")+".png"
            fs = FileSystemStorage()
            filename = fs.save(myfile, data)
            picLocation = UploadWellPictureModel.objects.create(picture=filename, name=name, well_nm=well_nm, radius=radius, depth=depth, level=level, village=village, district=district, state=state,pincode=pincode, lat=lat, lng=lng)
            picLocation.save()
            datauri= False
            del datauri
        except NameError:
            print("Image is not captured")
    else:
        form = UploadWellPictureForm()
    return render(request,'dashboard/capt_wells.html',{})

def uploadwellpic(request):
    if request.method == 'POST':
        form = UploadWellPictureForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('capt_wells')
    else:
        form = UploadWellPictureForm()
    return render(request,'dashboard/uploadWellPic.html',{})


def district_view(request):
    # Get the user response for district (replace 'user_district' with the actual user input)
    user_district = "Nashik"

    # Query the Features model to get the relevant district
    features = Features.objects.filter(district_name=user_district)

    # Query the Layers model to get the layers related to the district
    layers = Layers.objects.filter(features__district_name=user_district)

    # Render the data in a template or return it as a JSON response
    return render(request, 'dashboard/test.html', {'features': features, 'layers': layers})

def water_quality_form(request):
    if request.method == 'POST':
        form = quality_form(request.POST)
        if form.is_valid():
            # Extract form data
            print(request.POST['name'])
            name = request.POST['name']
            state = request.POST['state']
            district = request.POST['district']
            taluka = request.POST['taluka']
            village = request.POST['village']
            gram_panch = request.POST['gram_panch']
            water_quality = request.POST['water_quality']
            color= request.POST['color']
            odour= request.POST['odour']
            taste= request.POST['taste']
            ph = request.POST['ph']
            turbid = request.POST['turbid']
            hard = request.POST['hard']
            chloride = request.POST['chloride']
            alkaline = request.POST['alkaline']
            nitrate = request.POST['nitrate']
            fluoride = request.POST['fluoride']
            iron = request.POST['iron']
            chlorine = request.POST['chlorine']
            calcium = request.POST['calcium']
            magnesium = request.POST['magnesium']
            date = request.POST['date']
            
                # Create and save the model instance
            quality_model = water_quality_model(name=name, state=state, district=district, taluka=taluka,
                                                    village=village, gram_panch=gram_panch, water_quality=water_quality,
                                                    color=color,odour=odour,taste=taste,
                                                    ph=ph, turbid=turbid, hard=hard, chloride=chloride,
                                                    alkaline=alkaline, nitrate=nitrate, fluoride=fluoride,
                                                    iron=iron, chlorine=chlorine, calcium=calcium,
                                                    magnesium=magnesium, date=date)
            quality_model.save()
            messages.success(request, 'Form submitted successfully!')
            print('sucesss')
        # return redirect('success')  # Redirect to a success page after saving the data
        else:
            messages.success(request, 'Enter Correct Details!')
            form = quality_form()
    
    return render(request,'dashboard/water_quality_form.html',{})


def static_files_view(request):
    # static_folder = 'dashboard/static/'
    # folder_path = 'doc'
    # files = os.listdir(static_folder)
    # folder_full_path = os.path.join(static_folder, folder_path)
    # files = os.listdir(folder_full_path)
    documents=Document.objects.all()
    images = Image.objects.all()
    link=links.objects.all()
    context = {
        # 'files': files,
        # 'folder_path': folder_path,
        'documents':documents,
        'images': images,
        'links': link,
        
    }
    return render(request, 'dashboard/tutorial.html', context)

def water_related_forms(request):
    documents=Document.objects.all()

    context = {
        'documents':documents,        
    }
    return render(request, 'dashboard/water_related_forms.html', context)

def feature(request):
    if request.method == 'POST':
        form = features_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('water_related_forms')
    else:
        form = features_form()
    return render(request,'dashboard/feature.html',{})

def physical_feature(request):
    if request.method == 'POST':
        form = physical_features_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('water_related_forms')
    else:
        form = physical_features_form()
    return render(request,'dashboard/physical_feature.html',{})

def human_form(request):
    if request.method == 'POST':
        form = human_form_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('water_related_forms')
    else:
        form = human_form_form()
    return render(request,'dashboard/human_form.html',{})

def cultural(request):
    if request.method == 'POST':
        form = cultural_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('water_related_forms')
    else:
        form = cultural_form()
    return render(request,'dashboard/cultural.html',{})

def water_usable(request):
    if request.method == 'POST':
        form = water_usable_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.user = request.user
            instance.save()
            messages.success(request, "Registration successful." )
            print("data is saved.")
            return redirect('water_related_forms')
    else:
        form = water_usable_form()
    return render(request,'dashboard/water_usable.html',{})

def set_language(request):
    lang = request.GET.get('l', 'en')
    request.session[settings.LANGUAGE_SESSION_KEY] = lang
    # return to previous view
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # set cookies as well
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response

def index(request):
    output = _('Hello, world!')
    return HttpResponse(output)