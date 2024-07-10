from django.shortcuts import render,redirect
from .models import UploadWellPictureModel
from .models import Features
from .models import Layers
from .models import water_quality_model
from .models import links
from .models import MahaDemoV2126April24
from .models import MahaRiversFromOsmV116June23
from django.http import HttpResponse, Http404
from django.contrib.gis.geos import GEOSGeometry
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

import os, requests,json,io
# import pandas as pd
# import matplotlib.pyplot as plt
# from urllib.parse import quote



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

    # Fetch river names for the selected district
    river_names = get_river_names_for_district(user_district)

    context = {'wells': wells,'wellcount':wellcount,'features': features, 'layers': layers,'alllayers':Alllayers,'river_names': river_names,
        'district_name': user_district}
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

def get_layer(request):
    district = request.GET.get('district')
    print("district in get_layer function is ",district)
    if(district == 'Ahmadnagar'):
        district = 'Ahamadnagar'
    print("district is now ",district)
    layer = Layers.objects.filter(name__icontains=district, sub_title='drainage').first()
    if layer:
        print("layer name is  "+layer.name)
        print("layer value is  "+layer.value)
        layer_name = layer.value
        print(layer_name +" is layer name")
    else:
        layer_name = None
    return JsonResponse({'layer': layer_name})


def get_river_names_for_district(district_name):
    # district_name = request.GET.get('district')
    # print("district in get_river_names "+district_name)
    # Replace with your GeoNode's URL and appropriate parameters
    url = f'https://geonode.communitygis.in/geoserver//wfs'
    params = {
        'service': 'WFS',
        'version': '1.0.0',
        'request': 'GetFeature',
        'typeName': 'geonode:maha_rivers_withDistrict17june24',
        'outputFormat': 'application/json',
        'cql_filter': f"district='{district_name}'"
    }

    response = requests.get(url, params=params)
    data = response.json()
    # Extract river names
    river_names = sorted({feature['properties']['name'] for feature in data['features'] if 'name' in feature['properties'] and feature['properties']['name']})
    
    return river_names

def district_rivers_view(request, district_name):
    district_name = request.GET.get('district')

    print(district_name)
    if not district_name:
        return render(request, 'error_template.html', {'error_message': 'No district specified'})
    river_names = get_river_names_for_district(district_name)
    context = {
        'river_names': river_names,
        'district_name': district_name
    }
    return render(request, 'naturalfeatures.html', context)

# def get_villages_near_river(request):
#     river_name = request.GET.get('river_name')
#     print("Requested river name:", river_name)
    
#     # Replace with your GeoNode's URL and appropriate parameters
#     geonode_url = 'https://geonode.communitygis.in/geoserver/wfs'
#     params = {
#         'service': 'WFS',
#         'version': '1.0.0',
#         'request': 'GetFeature',
#         'typeName': 'geonode:maha_rivers_withDistrict17june24',
#         'outputFormat': 'application/json',
#         'cql_filter': f"name='{river_name}'"  # Adjust filter as per your data schema
#     }
    
#     try:
#         # Fetch river data from GeoNode
#         response = requests.get(geonode_url, params=params)
#         response.raise_for_status()  # Raise an exception for HTTP errors

#         river_data = response.json()
        
#         river_geometry = None  # Initialize river_geometry
        
#         for feature in river_data['features']:
#             if feature['properties']['name'] == river_name:
#                 print("River found")
#                 river_geometry = feature['geometry']
#                 print(river_geometry)
#                 break
        
#         # If river with given name not found
#         if river_geometry is None:
#             print(f"River '{river_name}' not found in GeoNode data.")
#             return JsonResponse({'error': f"River '{river_name}' not found in GeoNode data."}, status=404)

#         # Convert MultiLineString coordinates to WKT format
#         def multiline_to_wkt(multiline):
#             try:
#                 lines_str = ', '.join([
#                     f"({', '.join([f'{lon} {lat}' for lon, lat in line])})"
#                     for line in multiline if all(len(coord) == 2 for coord in line)
#                 ])
#                 return f"MULTILINESTRING({lines_str})"
#             except Exception as e:
#                 raise ValueError(f"Error in converting coordinates to WKT: {e}")

#         try:
#             river_geometry_wkt = multiline_to_wkt(river_geometry['coordinates'])
#         except ValueError as ve:
#             print(ve)
#             river_geometry_wkt = None

#         if river_geometry_wkt:
#             # Now fetch villages near the specified river using another GeoNode API endpoint
#             villages_geonode_url = 'https://geonode.communitygis.in/geoserver/wfs'
            
#             # Parameters for villages WFS GetFeature request
#             villages_params = {
#                 'service': 'WFS',
#                 'version': '1.0.0',
#                 'request': 'GetFeature',
#                 'typeName': 'geonode:maha_demo_v21_26april24',
#                 'outputFormat': 'application/json',
#                 'cql_filter': f"INTERSECTS(the_geom,MULTILINESTRING((74.4814618 20.1435521, 74.4811614 20.14325)))"
#             }
            
#             # Fetch villages data from GeoNode
#             villages_response = requests.get(villages_geonode_url, params=villages_params)
#             villages_response.raise_for_status()  # Raise an exception for HTTP errors

#             villages_data = villages_response.json()
#             print("Villages data:", villages_data)

#             # Extract relevant information from villages data
#             villages = []
#             for feature in villages_data.get('features', []):
#                 village_name = feature['properties'].get('area_name')  # Adjust based on your actual property name
#                 village_geom = feature.get('geometry')
#                 villages.append({
#                     'name': village_name,
#                     'geom': village_geom
#                 })
            
#             return JsonResponse({'villages': villages}, safe=False, status=200)  # Ensure to set a proper status code
    
#     except requests.exceptions.RequestException as e:
#         print(f"RequestException: {e}")
#         return JsonResponse({'error': f"Error fetching data from GeoNode: {e}"}, status=500)

#     except KeyError as e:
#         print(f"KeyError: {e}")
#         return JsonResponse({'error': f"KeyError: {e}"}, status=500)

#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return JsonResponse({'error': f"Unexpected error: {e}"}, status=500)


def intersecting_villages(request):
    river_name = request.GET.get('river_name')
    print(river_name)
    # Example: Find villages intersecting with a specific river
    river_id = 1  # Replace with the actual river ID you are interested in

    rivers = MahaRiversFromOsmV116June23.objects.filter(name=river_name)
    # for river in rivers:
    #     print(f"River Name: {river.geom}, ID: {river.fid}")
    if rivers.exists():
        # Handle the case where there are multiple rivers with the same name
        # For simplicity, you might choose the first one
        river = rivers.first()
        # return river.id
        intersecting_villages = MahaDemoV2126April24.objects.filter(geom__intersects=river.geom)

    # Optionally, you can perform further operations with intersecting_villages
        geojson_features = []
        for village in intersecting_villages:
            # print(village.area_name, "-", village.cen_2011)
            geom_geojson = village.geom.geojson  # Convert GEOSGeometry to GeoJSON
            
            geojson_feature = {
                'type': 'Feature',
                'geometry': geom_geojson,
                'properties': {
                    'area_name': village.area_name,
                    'cen_2011': village.cen_2011,
                    # Add other properties as needed
                }
            }
            geojson_features.append(geojson_feature)
            # print(geojson_features[0])
    # Return a response or render a template as needed
        return JsonResponse({'type': 'FeatureCollection', 'features': geojson_features})

    else:
        # Handle case where no river with the given name exists
        raise Http404("River with name '{}' does not exist".format(river_name))
        
def timeseries(request):
    # Load the data
    # file_path = "{% static 'data/healthdash/Dates_and_WaterLevel.csv' %}"
    file_path = os.path.join(settings.BASE_DIR,'dashboard', 'static', 'data', 'healthdash', 'Dates_and_WaterLevel.csv')
   
    data = pd.read_csv(file_path)

    # Convert the 'dates' column to datetime format
    data['Date'] = pd.to_datetime(data['dates'])

    # Filter the data for years after 2018
    data = data[data['Date'].dt.year > 2018]

    # Set the 'Date' column as the index
    data.set_index('Date', inplace=True)

    # Extract year from the 'Date' index
    data['Year'] = data.index.year

    # Plot the data
    plt.figure(figsize=(10, 6))
    for year, group in data.groupby('Year'):
        plt.plot(group.index, group['water area(hectares)'], marker='o', linestyle='-', label=str(year))

    plt.title('Water Level Over Time')
    plt.xlabel('Date')
    plt.ylabel('Water Level (hectares)')
    plt.legend(title='Year')
    plt.grid(True)

    # Improve date formatting on x-axis
    plt.gcf().autofmt_xdate()

    # Save the plot to a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    
    # Encode the PNG image to base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    # Pass the image to the template
    return render(request, 'dashboard/timeseries.html', {'graph': graph})