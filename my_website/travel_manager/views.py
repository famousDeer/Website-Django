import folium

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from datetime import timedelta
from datetime import datetime

from .models import Destinations, Tiktok, Instagram, Information, Location_address, Planner_Date, Planner_Descriptions
from .forms import CreateNewDestination, DateForm
from .utils.utils import find_location_coordinates, different_days_in_db


# Creating class views

class AddAddressPoint(View):

    view_name = 'info-destination'
    icons = {"Attraction": ["location-pin", "blue"],
                 "Museum": ["landmark", "orange"],
                 "Parks": ["tree", "green"],
                 "Restaurant": ["burger", "red"],
                 "Shops": ["shop", "purple"]}

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        return redirect(reverse(self.view_name, args=[destination.id]))

    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        submitted_address = request.POST.get("add_address")
        object_type = request.POST.get("object_type")

        if not submitted_address:
            messages.error(request, "You need to write an address")
        elif object_type == "Choose object type":
            messages.error(request, "You need to choose object type")
        else:
            loc_coordinates = find_location_coordinates(submitted_address)
            if loc_coordinates is None:
                messages.error(request, "Wrong address")
            else:
                _ = Location_address.objects.create(destinations=destination,
                                                    address=loc_coordinates['address'],
                                                    latitude=loc_coordinates['latitude'],
                                                    longitude=loc_coordinates['longitude'],
                                                    icon=self.icons[object_type][0],
                                                    marker_color=self.icons[object_type][1])
                
        return redirect(reverse(self.view_name, args=[destination.id]))

class AddDescription(View):
    view_name = "info-destination"

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        return redirect(reverse(self.view_name, args=[destination.id]))

    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        information = Information.objects.filter(destinations=destination).first()
        description = request.POST.get(f"descriptions{id}")

        if information is not None:
            information.description = description
            information.save()
            return redirect(reverse(self.view_name, args=[destination.id]))
        else:
            localization = find_location_coordinates(f"{destination.city, destination.country.name}")
            latitude = localization["latitude"]
            longitude = localization["longitude"]
            information = Information.objects.create(destinations=destination, 
                                                     fly_cost=0.0, 
                                                     description=description,)
        return redirect(reverse(self.view_name, args=[destination.id]))
     
class AddDestination(View):
    template_name = "main/add_destination.html"
    view_name = "travel-manager"

    def get(self, request):
        form = CreateNewDestination()
        return render(request, self.template_name, {"form":form})
    
    def post(self, request):
        form = CreateNewDestination(request.POST)

        if form.is_valid():
            country_code = form.cleaned_data["country"]
            city = form.cleaned_data["city"]
            tiktok = form.cleaned_data["tiktok"]
            instagram = form.cleaned_data["instagram"]
            coordinates = find_location_coordinates({"city":city, "country_code": country_code}, featuretype="city")

            destination = Destinations(country=country_code,
                                       city=city,
                                       latitude=coordinates["latitude"],
                                       longitude=coordinates["longitude"])
            tiktok = Tiktok(destinations=destination, link=tiktok)
            instagram = Instagram(destinations=destination, link=instagram)

            destination.save()
            tiktok.save()
            instagram.save()
            request.user.destination.add(destination)

        return redirect(reverse(self.view_name))
    
class DeleteDestination(View):
    temple_name = "travel-manager"

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        messages.info(request, f"Successfully deleted {destination.country.name} | {destination.city}")
        destination.delete()
        return redirect(reverse(self.temple_name))

class InfoDestination(View):
    temple_name = "main/info_destination.html"

    def get(self, request, id):
        destination = Destinations.objects.get(id=id) 
        information = Information.objects.filter(destinations=destination).first()
        location_address = Location_address.objects.filter(destinations=destination).all()
        interactive_map = folium.Map(location=[destination.latitude, destination.longitude], zoom_start=14)
        folium.Marker((destination.latitude, destination.longitude),
                      icon=folium.Icon(color='blue', prefix='fa')
                      ).add_to(interactive_map)
        if location_address is not None:
            for location in location_address:
                folium.Marker((location.latitude, location.longitude),
                              popup=location.address,
                              icon=folium.Icon(color=location.marker_color, icon=location.icon, prefix='fa')
                              ).add_to(interactive_map)

        return render(request, self.temple_name, {"destinations":destination, "information": information, "map": interactive_map._repr_html_})

class PlannerView(View):
    template_name = 'main/planner.html'
    colors = {"rgb(0, 0, 255)":"#3395db",
              "rgb(255, 165, 0)":"#e39608",
              "rgb(0, 128, 0)":"#23b82f",
              "rgb(255, 0, 0)":"#bc2c2c",
              "rgb(128, 0, 128)":"#9d32d6"}

    def get(self, request, id):
        destination_db = Destinations.objects.get(id=id)
        location_address = Location_address.objects.filter(destinations=destination_db).all()
        planner_db = Planner_Date.objects.filter(destinations=destination_db).first()
        initial_data = {}
        
        if planner_db:
            initial_data["start_date"] = planner_db.start_date
            initial_data["end_date"] = planner_db.end_date
            planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()
        else:
            planner_daily_db = Planner_Descriptions.objects.none()

        form = DateForm(initial=initial_data)
        return render(request, self.template_name, {"destinations": destination_db,
                                                    "form": form,
                                                    "planner_info": planner_daily_db,
                                                    "locations": location_address})

    def post(self, request, id):
        destination_db = Destinations.objects.get(id=id)
        location_address = Location_address.objects.filter(destinations=destination_db).all()
        planner_db = Planner_Date.objects.filter(destinations=destination_db).first()
        initial_data = {}
        if planner_db:
            planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()
            initial_data["start_date"] = planner_db.start_date
            initial_data["end_date"] = planner_db.end_date
        else:
            planner_daily_db = Planner_Descriptions.objects.none()

        form = DateForm(request.POST, initial=initial_data)

        if form.is_valid():
            if planner_db:
                if different_days_in_db(planner_db, form):
                    for locations in location_address:
                        locations.inside_planner = False
                        locations.save()
                    planner_db.start_date = form.cleaned_data["start_date"]
                    planner_db.end_date = form.cleaned_data["end_date"]
                    planner_db.save()
                    Planner_Descriptions.objects.filter(planner_date=planner_db).delete() # Clear table from any data
                    time_difference = planner_db.end_date - planner_db.start_date
                    for i in range(time_difference.days + 1):
                        Planner_Descriptions.objects.create(planner_date=planner_db,
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
                    Planner_Descriptions.objects.create(planner_date=planner_db,
                                                        date=planner_db.start_date + timedelta(days=i),
                                                        descriptions="")
                planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()

        else:
            table_date = request.POST.get('table_header')
            try:
                date = datetime.strptime(table_date, "%b %d, %Y")
            except ValueError:
                date = datetime.strptime(table_date, "%b. %d, %Y")
            formatted_date = date.strftime("%Y-%m-%d")
            location = Location_address.objects.filter(destinations_id=destination_db, id=request.POST.get('id')).first()
            location.inside_planner = True
            location.save()
            planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id, date=formatted_date).first()
            planner_daily_db.descriptions += request.POST.get('text') + ":" + self.colors[request.POST.get('color')] + ";"
            planner_daily_db.save()
            planner_daily_db = Planner_Descriptions.objects.filter(planner_date_id=planner_db.id).all()

        return render(request, self.template_name, {"destinations": destination_db,
                                                    "form": form,
                                                    "planner_info": planner_daily_db,
                                                    "locations": location_address})

# Create your views here.

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
