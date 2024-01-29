from django.urls import path
from . import views

urlpatterns = [
    path('travel-manager', views.travel_manager, name='travel-manager'),
    path('add-destination', views.add_destination, name='add-destination'),
    path('travel-manager/<int:id>', views.index, name='info-destination'),
    path('travel-manager/delete/<int:id>', views.delete, name='delete'),
    path('travel-manager/add-description/<int:id>', views.add_description, name='add_description'),
    path('travel-manager/add-address-point/<int:id>', views.add_address_point, name='add_address_point'),
    path('travel-manager/tiktok/<int:id>', views.tiktok, name='tiktok'),
    path('travel-manager/planner/<int:id>', views.planner, name='planner'),
]
