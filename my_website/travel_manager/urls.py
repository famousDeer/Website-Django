from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('travel-manager', login_required(views.TravelManagerView.as_view(), login_url='login'), name='travel-manager'),
    path('travel-manager/add-destination', login_required(views.AddDestination.as_view(), login_url='login'), name='add-destination'),
    path('travel-manager/<int:id>', login_required(views.InfoDestination.as_view(), login_url='login'), name='info-destination'),
    path('travel-manager/delete/<int:id>', login_required(views.DeleteDestination.as_view(), login_url='login'), name='delete'),
    path('travel-manager/add-description/<int:id>', login_required(views.AddDescription.as_view(), login_url='login'), name='add_description'),
    path('travel-manager/add-address-point/<int:id>', login_required(views.AddAddressPoint.as_view(), login_url='login'), name='add_address_point'),
    path('travel-manager/tiktok/<int:id>', login_required(views.TikTokView.as_view(), login_url='login'), name='tiktok'),
    path('travel-manager/planner/<int:id>', login_required(views.PlannerView.as_view(), login_url='login'), name='planner'),
    path('travel-manager/documents/<int:id>', login_required(views.DocumentsView.as_view(), login_url='login'), name='documents'),
    path('travel-manager/budget/<int:id>', login_required(views.BudgetView.as_view(), login_url='login'), name='budget'),
    path('travel-manager/documents/open-file/<int:id>/', login_required(views.DocumentsView.as_view(), login_url='login'), name='open-file'),
    path('travel-manager/back-page', views.back_page, name='back-page'),
]
