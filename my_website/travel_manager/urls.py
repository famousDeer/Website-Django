from django.urls import path
from . import views

urlpatterns = [
    path('travel-manager', views.TravelManagerView.as_view(), name='travel-manager'),
    path('add-destination', views.AddDestination.as_view(), name='add-destination'),
    path('travel-manager/<int:id>', views.InfoDestination.as_view(), name='info-destination'),
    path('travel-manager/delete/<int:id>', views.DeleteDestination.as_view(), name='delete'),
    path('travel-manager/add-description/<int:id>', views.AddDescription.as_view(), name='add_description'),
    path('travel-manager/add-address-point/<int:id>', views.AddAddressPoint.as_view(), name='add_address_point'),
    path('travel-manager/tiktok/<int:id>', views.TikTokView.as_view(), name='tiktok'),
    path('travel-manager/planner/<int:id>', views.PlannerView.as_view(), name='planner'),
    path('travel-manager/documents/<int:id>', views.DocumentsView.as_view(), name='documents'),
    path('travel-manager/budget/<int:id>', views.BudgetView.as_view(), name='bugdet'),
]
