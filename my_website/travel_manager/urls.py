from django.urls import path
from . import views

urlpatterns = [
    path('travel-manager', views.travel_manager, name='travel-manager'),
    path('add-destination', views.add_destination, name='add-destination'),
    path('travel-manager/<int:id>', views.index, name='info-destination'),
]
