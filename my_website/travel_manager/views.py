from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Destinations, Tiktok, Instagram, Information
from .forms import CreateNewDestination

# Create your views here.

def add_description(request, id):
    if request.method == "POST":
        destination = Destinations.objects.get(id=id)
        information = Information.objects.filter(destinations=destination).first()
        description = request.POST.get(f"descriptions{id}")
        if information is not None:
            information.description = description
            information.save()
        else:
            information = Information.objects.create(destinations=destination, fly_cost=0.0, description=description)
    return render(request, 'main/info_destination.html', {"destinations":destination, "information": information})

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
            
            destination.save()
            tiktok.save()
            instagram.save()
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

def travel_manager(request):
    #TODO: Render information from database
    return render(request, "main/travel_manager.html")

def index(request, id):
    destination = Destinations.objects.get(id=id) 
    information = Information.objects.filter(destinations=destination).first()
    return render(request, "main/info_destination.html", {"destinations":destination, "information": information})

