from django.contrib import admin
from .models import Destinations, Tiktok, Information, Location_address, Planner_Date, Planner_Table_Date, Planner_Table_Descriptions, Documents

# Register your models here.
admin.site.register(Destinations)
admin.site.register(Information)
admin.site.register(Tiktok)
admin.site.register(Location_address)
admin.site.register(Planner_Date)
admin.site.register(Planner_Table_Date)
admin.site.register(Planner_Table_Descriptions)
admin.site.register(Documents)
