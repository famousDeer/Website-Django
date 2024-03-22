import folium
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.http import FileResponse
from datetime import timedelta
from datetime import datetime

from .models import Destinations, Tiktok, Information, Location_address, Planner_Date, Planner_Table_Date, Planner_Table_Descriptions, Documents, Budget
from .forms import CreateNewDestination, DateForm, DocumentsForm, BudgetForm
from .utils.utils import find_location_coordinates, different_days_in_db, get_cleared_url
from utils.messages import Message


# Creating class views

class AddAddressPoint(View):

    view_name = 'info-destination'
    icons = {"Attraction": ["location-pin", "blue"],
                 "Museum": ["landmark", "orange"],
                 "Parks": ["tree", "green"],
                 "Restaurant": ["burger", "red"],
                 "Shops": ["shop", "purple"]}
    message = Message()

    def __wrong_object_type(self, object_type):
        objects_list = ["Attraction", "Museum", "Parks", "Restaurant", "Shops"]
        return object_type not in objects_list
            
    def __empty_address_field(self, address):
        return not address
            
    def __not_found_address(self, loc_coordinates):
        return loc_coordinates is None
    
    def __submitted_price(self, price):
        return price
    
    def __submitted_description(self, description):
        return description

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        return redirect(reverse(self.view_name, args=[destination.id]))

    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        submitted_address = request.POST.get("add_address")
        object_type = request.POST.get("object_type")
        description = request.POST.get("address_description")
        price = request.POST.get("price")

        if self.__empty_address_field(submitted_address):
            self.message.error(request, "You need to write an address")
        elif self.__wrong_object_type(object_type):
            self.message.error(request, "You need to choose object type")
        else:
            loc_coordinates = find_location_coordinates(submitted_address)
            if self.__not_found_address(loc_coordinates):
                self.message.error(request, "Wrong address")
            else:
                location_address = Location_address.objects.create(destinations=destination,
                                                                   address=loc_coordinates['address'],
                                                                   latitude=loc_coordinates['latitude'],
                                                                   longitude=loc_coordinates['longitude'],
                                                                   icon=self.icons[object_type][0],
                                                                   marker_color=self.icons[object_type][1],
                                                                   descriptions=object_type)
                if self.__submitted_price(price):
                    location_address.price = price

                if self.__submitted_description(description):
                    location_address.descriptions = description
                location_address.save()
                
        return redirect(reverse(self.view_name, args=[destination.id]))

class AddDescription(View):
    view_name = "info-destination"
    message = Message()

    def __information_table_exist(self, table):
        return table is not None

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        return redirect(reverse(self.view_name, args=[destination.id]))

    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        information = Information.objects.filter(destinations=destination).first()
        description = request.POST.get(f"descriptions{id}")

        if self.__information_table_exist(information):
            information.description = description
            information.save()
            self.message.success(request, "Saved successfully")
            return redirect(reverse(self.view_name, args=[destination.id]))
        else:
            information = Information.objects.create(destinations=destination, 
                                                     fly_cost=0.0, 
                                                     description=description,)
        return redirect(reverse(self.view_name, args=[destination.id]))
     
class AddDestination(View):
    #TODO City finder, find new library
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
            coordinates = find_location_coordinates({"city":city, "country_code": country_code}, featuretype="city")

            destination = Destinations(country=country_code,
                                       city=city,
                                       latitude=coordinates["latitude"],
                                       longitude=coordinates["longitude"])

            destination.save()
            request.user.destination.add(destination)

        return redirect(reverse(self.view_name))
    
class DeleteDestination(View):
    temple_name = "travel-manager"
    message = Message()

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        destination.delete()
        self.message.success(request, f"Successfully deleted {destination.country.name} | {destination.city}")
        return redirect(reverse(self.temple_name))

class InfoDestination(View):
    temple_name = "main/info_destination.html"

    def get(self, request, id):
        destination = Destinations.objects.get(id=id) 
        information = Information.objects.filter(destinations=destination).first()
        location_address = Location_address.objects.filter(destinations=destination).all()
        interactive_map = folium.Map(location=[destination.latitude, destination.longitude], zoom_start=14, scrollWheelZoom=False)
        if location_address is not None:
            for location in location_address:
                folium.Marker((location.latitude, location.longitude),
                              popup=location.descriptions,
                              icon=folium.Icon(color=location.marker_color, icon=location.icon, prefix='fa')
                              ).add_to(interactive_map)

        context = {
            "destinations": destination,
            "information": information,
            "map": interactive_map._repr_html_
        }
        return render(request, self.temple_name, context)

class PlannerView(View):
    template_name = 'main/planner.html'
    colors = {"rgb(0, 0, 255)":"#3395db",
              "rgb(255, 165, 0)":"#e39608",
              "rgb(0, 128, 0)":"#23b82f",
              "rgb(255, 0, 0)":"#bc2c2c",
              "rgb(128, 0, 128)":"#9d32d6"}

    def __get_info_from_db(self, id):
        destination_db = Destinations.objects.get(id=id)
        location_address = Location_address.objects.filter(destinations=destination_db).all()
        planner_date = Planner_Date.objects.filter(destinations=destination_db).first()
        
        return destination_db, location_address, planner_date
    
    def __get_initial_date(self, planner_date):
        initial_data = {}
        if planner_date:
            initial_data["start_date"] = planner_date.start_date
            initial_data["end_date"] = planner_date.end_date
            planner_table_date = Planner_Table_Date.objects.filter(planner_date_id=planner_date.id).all()
        else:
            planner_table_date = Planner_Table_Date.objects.none()

        return initial_data, planner_table_date
    
    def __create_date_range(self, planner_date):
        time_difference = planner_date.end_date - planner_date.start_date
        for i in range(time_difference.days + 1):
            Planner_Table_Date.objects.create(planner_date=planner_date,
                                              date=planner_date.start_date + timedelta(days=i))

        return Planner_Table_Date.objects.filter(planner_date_id=planner_date.id).all()

    def get(self, request, id):
        destination_db, location_address, planner_date = self.__get_info_from_db(id)
        initial_data, planner_table_date = self.__get_initial_date(planner_date)
        form = DateForm(initial=initial_data)

        context = {
            "destinations": destination_db,
            "form": form,
            "planner_table_dates": planner_table_date,
            "locations": location_address}
        return render(request, self.template_name, context)

    def post(self, request, id):
        destination_db, location_address, planner_date = self.__get_info_from_db(id)
        initial_data, planner_table_date = self.__get_initial_date(planner_date)
        form = DateForm(request.POST, initial=initial_data)

        if form.is_valid():
            if planner_date:
                if different_days_in_db(planner_date, form):
                    for locations in location_address:
                        locations.inside_planner = False
                        locations.save()
                    planner_date.start_date = form.cleaned_data["start_date"]
                    planner_date.end_date = form.cleaned_data["end_date"]
                    planner_date.save()
                    Planner_Table_Date.objects.filter(planner_date=planner_date).delete() # Clear table from any data
                    planner_table_date = self.__create_date_range(planner_date)
            else:
                planner_date = Planner_Date.objects.create(destinations=destination_db,
                                                           start_date=form.cleaned_data["start_date"],
                                                           end_date=form.cleaned_data["end_date"])
                planner_table_date = self.__create_date_range(planner_date)

        else:
            table_date = request.POST.get('table_header')
            try:
                date = datetime.strptime(table_date, "%B %d, %Y")
            except ValueError:
                date = datetime.strptime(table_date, "%b. %d, %Y")
            formatted_date = date.strftime("%Y-%m-%d")
            location = Location_address.objects.filter(destinations_id=destination_db, id=request.POST.get('id')).first()
            location.inside_planner = True
            location.save()
            planner_table_date = Planner_Table_Date.objects.get(planner_date_id=planner_date.id, date=formatted_date)
            planner_table_description = Planner_Table_Descriptions.objects.create(planner_table_date=planner_table_date,
                                                                                  location_address=location,
                                                                                  descriptions=request.POST.get('text'),
                                                                                  color_label=self.colors[request.POST.get('color')])
            planner_table_date = Planner_Table_Date.objects.filter(planner_date_id=planner_date.id).all()
        
        context = {
            "destinations": destination_db,
            "form": form,
            "planner_table_dates": planner_table_date,
            "locations": location_address}
        
        return render(request, self.template_name, context)

class TikTokView(View):
    template_name = "main/tiktok.html"
    view_name = "tiktok"
    message = Message()

    def get(self, request, id):
        destination = Destinations.objects.get(id=id)
        tiktok = Tiktok.objects.filter(destinations=destination).all()
        return render(request, self.template_name, {"tiktok_link":tiktok})

    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        delete_id = request.POST.get("delete")
        if request.POST.get("newItem"):
            text = get_cleared_url(request.POST.get("new"))
            if len(text.split("/")[-1]) < 19:
                self.message.error(request, "Wrong address, clear box and look at example")
            else:
                tiktok = Tiktok.objects.create(destinations=destination,
                                               link=text)

            return redirect(reverse(self.view_name, args=[id]))
        elif delete_id:
            tiktok = Tiktok.objects.get(id=delete_id)
            messages.info(request, f"Successfully deleted {tiktok.link}")
            tiktok.delete()
        
        return redirect(reverse(self.view_name, args=[id]))
        
class TravelManagerView(View):
    template_name = "main/travel_manager.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
class DocumentsView(View):
    template_name = "main/documents.html"
    view_name = "documents"
    message = Message()

    def get(self, request, id):
        form = DocumentsForm()
        documents = Documents.objects.filter(destinations_id=id).all()
        if "open-file" in request.path:
            document = Documents.objects.filter(id=id).first()
            return FileResponse(document.file, content_type='application/pdf')
        return render(request, self.template_name, {'form': form, 'documents': documents})
    
    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        form = DocumentsForm(request.POST, request.FILES)
        delete_id = request.POST.get("delete_id")

        if form.is_valid():
            documents = form.save(commit=False)
            documents.destinations = destination
            documents.save()
            return redirect(reverse(self.view_name, args=[id]))
        elif delete_id:
            budget = Documents.objects.get(id=delete_id)
            budget.delete()
            self.message.success(request, f"Successfully deleted '{budget.description}'")
            return redirect(reverse(self.view_name, args=[id]))
    
        return render(request, self.template_name, {'form': form})

        # try:
            # return FileResponse(open('Media/cv_ENG.pdf', 'rb'), content_type='application/pdf')
        # except FileNotFoundError:

class BudgetView(View):
    template_name = "main/budget.html"
    view_name = "budget"
    message = Message()

    def get(self, request, id):
        form = BudgetForm()
        budget = Budget.objects.filter(destinations_id=id).all()
        return render(request, self.template_name, {"form": form, "budgets": budget})

    def post(self, request, id):
        destination = Destinations.objects.get(id=id)
        form = BudgetForm(request.POST)
        delete_id = request.POST.get("delete_id")

        if form.is_valid():
            budget = form.save(commit=False)
            budget.destinations = destination
            budget.save()
        
        elif delete_id:
            budget = Budget.objects.get(id=delete_id)
            budget.delete()
            self.message.success(request, f"Successfully deleted '{budget.description}'")
        
        return redirect(reverse(self.view_name, args=[id]))
    
def back_page(request):
    view_name = 'info-destination'
    id = request.META['HTTP_REFERER'][-1]
    return redirect(reverse(view_name, args=[id]))
