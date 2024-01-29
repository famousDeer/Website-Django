from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Destinations, Tiktok, Instagram, Information, Location_address, Planner_Date, Planner_Descriptions
from .forms import CreateNewDestination, DateForm
import folium
from folium.plugins import Geocoder
from geopy.geocoders import Nominatim
from datetime import timedelta


# Create your views here.

def add_address_point(request, id):
    destination = Destinations.objects.get(id=id)
    location_address = Location_address.objects.filter(destinations=destination).first()
    icons = {"Attraction": ["location-pin", "blue"],
             "Museum": ["landmark", "orange"],
             "Parks": ["tree", "green"],
             "Restaurant": ["burger", "red"],
             "Shops": ["shop", "purple"]}
    
    if request.method == "POST":
        submitted_address = request.POST.get("add_address")
        object_type = request.POST.get("object_type")
        if submitted_address == '':
            messages.error(request, "You need to write an address")
        elif object_type == 'Choose object type':
            messages.error(request, "You need to choose object type")
        else:
            localization = find_location_coordinates(submitted_address)
            if localization is None:
                messages.error(request, "Wrong address")
            else:
                location_address = Location_address.objects.create(destinations=destination,
                                                                   address=localization["address"],
                                                                   latitude=localization["latitude"],
                                                                   longitude=localization["longitude"],
                                                                   icon=icons[object_type][0],
                                                                   marker_color=icons[object_type][1])
    
        return redirect(reverse('info-destination', args=[destination.id]))

def add_description(request, id):

    destination = Destinations.objects.get(id=id)
    information = Information.objects.filter(destinations=destination).first()

    if request.method == "POST":
        description = request.POST.get(f"descriptions{id}")
        if information is not None:
            information.description = description
            information.save()
    return redirect(reverse('info-destination', args=[destination.id]))

def add_destination(request):
    if request.method == "POST":
        form = CreateNewDestination(request.POST)
        
        if form.is_valid():
            country_code = form.cleaned_data["country"]
            city = form.cleaned_data["city"]
            tiktok = form.cleaned_data["tiktok"]
            instagram = form.cleaned_data["instagram"]

            
            destination = Destinations(country=country_code,
                                       city=city)
            tiktok = Tiktok(destinations=destination, link=tiktok)
            instagram = Instagram(destinations=destination, link=instagram)

            localization = find_location_coordinates(f"{destination.city, destination.country.name}")
            latitude = localization["latitude"]
            longitude = localization["longitude"]

            information = Information(destinations=destination, 
                                      fly_cost=0.0, 
                                      description="",
                                      latitude=latitude,
                                      longitude=longitude)
            destination.save()
            tiktok.save()
            instagram.save()
            information.save()
            request.user.destination.add(destination)

        return HttpResponseRedirect("travel-manager")
    else:
        form = CreateNewDestination()

    return render(request, "main/add_destination.html", {"form":form})

def delete(request, id):
    destination = Destinations.objects.get(id=id)
    messages.info(request, f"Successfully deleted {destination.country.name}")
    destination.delete()

    return redirect(reverse('travel-manager'))

def index(request, id):
    destination = Destinations.objects.get(id=id) 
    information = Information.objects.filter(destinations=destination).first()
    location_address = Location_address.objects.filter(destinations=destination).all()
    interactive_map = folium.Map(location=[information.latitude, information.longitude], zoom_start=14)
    folium.Marker((information.latitude, information.longitude),
                  icon=folium.Icon(color='blue', icon='location-pin', prefix='fa')).add_to(interactive_map)
    if location_address is not None:
        for location in location_address:
            folium.Marker((location.latitude, location.longitude),
                          popup=location.address,
                          icon=folium.Icon(color=location.marker_color, icon=location.icon, prefix='fa')).add_to(interactive_map)

    return render(request, "main/info_destination.html", {"destinations":destination, "information": information, "map": interactive_map._repr_html_})

def planner(request, id):
    destination_db = Destinations.objects.get(id=id)
    location_address = Location_address.objects.filter(destinations=destination_db).all()
    planner_db = Planner_Date.objects.filter(destinations=destination_db).first()
    initial_data={}
    if planner_db:
        initial_data["start_date"] = planner_db.start_date
        initial_data["end_date"] = planner_db.end_date
        planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()
    else:
        planner_daily_db = Planner_Descriptions.objects.none()
    
    form = DateForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        if planner_db:
            if different_days_in_db(planner_db, form):     
                planner_db.start_date = form.cleaned_data["start_date"]
                planner_db.end_date = form.cleaned_data["end_date"]
                Planner_Descriptions.objects.all().delete()
                time_difference = planner_db.end_date - planner_db.start_date
                for i in range(time_difference.days + 1):
                    planner_daily_db = Planner_Descriptions.objects.create(planner_date=planner_db,
                                                                           date=planner_db.start_date + timedelta(days=i),
                                                                           descriptions="")
                planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()
                    
        else:
            planner_db = Planner_Date(destinations=destination_db,
                                 start_date=form.cleaned_data["start_date"],
                                 end_date=form.cleaned_data["end_date"])
            planner_db.save()
            time_difference = planner_db.end_date - planner_db.start_date
            for i in range(time_difference.days + 1):
                planner_daily_db = Planner_Descriptions.objects.create(planner_date=planner_db,
                                                                       date=planner_db.start_date + timedelta(days=i),
                                                                       descriptions="")
            planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()
    return render(request, "main/planner.html",{"destinations":destination_db, "form":form, "planner_info": planner_daily_db, "locations": location_address})

def tiktok(request, id):
    destination = Destinations.objects.get(id=id)

    if request.method == "POST":
        if request.POST.get("newItem"):
            text = request.POST.get("new")
            if len(text.split("/")[-1]) < 19:
                messages.error(request, "Wrong address, clear box and look at example")
            else:
                destination.tiktok_set.create(link=text)
    return render(request, "main/tiktok.html", {"tiktok_link":destination.tiktok_set.all()})

def travel_manager(request):
    return render(request, "main/travel_manager.html")

def find_location_coordinates(address):
    nomination = Nominatim(user_agent="http://127.0.0.1:8000/")
    localization = nomination.geocode(address, exactly_one=False)

    if localization is None:
        return None
    
    localization = localization[0]

    return {"latitude": localization.latitude,
            "longitude": localization.longitude,
            "address": localization.address}

def different_days_in_db(db, days):
    if db.start_date == days.cleaned_data["start_date"] and db.end_date == days.cleaned_data["end_date"]:
        return False
    
    return True