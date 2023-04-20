from django.shortcuts import render,redirect
from .models import UploadWellPictureModel
from django.contrib import messages
import re,base64,time
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.gis.geos import Point
from .forms import UploadWellPictureForm

def HomePage(request):
    return render(request, "HomePage.html")

def Dash(request):
    return render(request, "dashboard/dash.html")

def map(request):
    return render(request, "dashboard/map.html") 

def watergis(request):
    wells = UploadWellPictureModel.objects.all()
    wellcount = UploadWellPictureModel.objects.count()
    context = {'wells': wells,'wellcount':wellcount}
    return render(request,'dashboard/watergis.html',context)

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


    