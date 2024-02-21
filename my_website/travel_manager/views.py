import folium

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
        address_description = request.POST.get("address_description")
        price = request.POST.get("price")

        if not submitted_address:
            messages.error(request, "You need to write an address")
        elif object_type == "Choose object type":
            messages.error(request, "You need to choose object type")
        else:
            loc_coordinates = find_location_coordinates(submitted_address)
            if loc_coordinates is None:
                messages.error(request, "Wrong address")
            else:
                location_address = Location_address.objects.create(destinations=destination,
                                                                   address=loc_coordinates['address'],
                                                                   latitude=loc_coordinates['latitude'],
                                                                   longitude=loc_coordinates['longitude'],
                                                                   icon=self.icons[object_type][0],
                                                                   marker_color=self.icons[object_type][1],
                                                                   descriptions=object_type)
        if price != '':
            location_address.price = price
        
        if address_description != '':
            location_address.descriptions = address_description
        
        location_address.save()
                
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
            coordinates = find_location_coordinates({"city":city, "country_code": country_code}, featuretype="city")

            destination = Destinations(country=country_code,
                                       city=city,
                                       latitude=coordinates["latitude"],
                                       longitude=coordinates["longitude"])
            if tiktok != '':
                tiktok = Tiktok(destinations=destination, link=tiktok)
                tiktok.save()

            destination.save()
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
        # folium.Marker((destination.latitude, destination.longitude),
        #               icon=folium.Icon(color='blue', prefix='fa')
        #               ).add_to(interactive_map)
        if location_address is not None:
            for location in location_address:
                folium.Marker((location.latitude, location.longitude),
                              popup=location.descriptions,
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

    def get_info_from_db(self, id):
        destination_db = Destinations.objects.get(id=id)
        location_address = Location_address.objects.filter(destinations=destination_db).all()
        planner_date = Planner_Date.objects.filter(destinations=destination_db).first()
        
        return destination_db, location_address, planner_date
    
    def get_initial_date(self, planner_date):
        initial_data = {}
        if planner_date:
            initial_data["start_date"] = planner_date.start_date
            initial_data["end_date"] = planner_date.end_date
            planner_table_date = Planner_Table_Date.objects.filter(planner_date_id=planner_date.id).all()
        else:
            planner_table_date = Planner_Table_Date.objects.none()

        return initial_data, planner_table_date
    
    def create_date_range(self, planner_date):
        time_difference = planner_date.end_date - planner_date.start_date
        for i in range(time_difference.days + 1):
            Planner_Table_Date.objects.create(planner_date=planner_date,
                                              date=planner_date.start_date + timedelta(days=i))

        return Planner_Table_Date.objects.filter(planner_date_id=planner_date.id).all()

    def get(self, request, id):
        destination_db, location_address, planner_date = self.get_info_from_db(id)
        initial_data, planner_table_date = self.get_initial_date(planner_date)
        form = DateForm(initial=initial_data)

        return render(request, self.template_name, {"destinations": destination_db,
                                                    "form": form,
                                                    "planner_table_dates": planner_table_date,
                                                    "locations": location_address})

    def post(self, request, id):
        destination_db, location_address, planner_date = self.get_info_from_db(id)
        initial_data, planner_table_date = self.get_initial_date(planner_date)
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
                    planner_table_date = self.create_date_range(planner_date)
            else:
                planner_date = Planner_Date.objects.create(destinations=destination_db,
                                                           start_date=form.cleaned_data["start_date"],
                                                           end_date=form.cleaned_data["end_date"])
                planner_table_date = self.create_date_range(planner_date)

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

        return render(request, self.template_name, {"destinations": destination_db,
                                                    "form": form,
                                                    "planner_table_dates": planner_table_date,
                                                    "locations": location_address})

class TikTokView(View):
    template_name = "main/tiktok.html"
    view_name = "tiktok"

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
                messages.error(request, "Wrong address, clear box and look at example")
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

        if form.is_valid():
            documents = form.save(commit=False)
            documents.destinations = destination
            documents.save()
            return redirect(reverse(self.view_name, args=[id]))
    
        return render(request, self.template_name, {'form': form})

        # try:
            # return FileResponse(open('Media/cv_ENG.pdf', 'rb'), content_type='application/pdf')
        # except FileNotFoundError:

class BudgetView(View):
    template_name = "main/budget.html"
    view_name = "budget"

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
        
        return redirect(reverse(self.view_name, args=[id]))
