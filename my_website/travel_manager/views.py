from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Destinations, Tiktok, Instagram
from .forms import CreateNewDestination

# Create your views here.
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

def travel_manager(request):
    #TODO: Render information from database
    return render(request, "main/travel_manager.html")

def index(request, id):
    destinations = Destinations.objects.get(id=id)
    return render(request, "main/info_destination.html", {"destinations": destinations})


