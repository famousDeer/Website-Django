import folium

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import ToDoList
from .forms import CreateNewList
from utils.messages import Message

# Create your views here.
class ToDoListView(View):
    template_name = "todolist/view.html"
    message = Message()
    
    def get(self, request):
        context = {
            "form": CreateNewList(),
            "user_lists": request.user.todolist.all(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CreateNewList(request.POST)
        delete_id = request.POST.get("delete_id")
        
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()
            
            self.message.success(request, f"New to-do list '{new_list.name}' created successfully")
            return redirect(f"/{new_list.id}")
        
        elif delete_id:
            try:
                td_list = ToDoList.objects.get(id=delete_id)
                td_list.delete()
                self.message.info(request, f"Successfully deleted '{td_list.name}'")
            except ToDoList.DoesNotExist:
                Message.error(request, "To-do list not found")   

        return redirect('view')

class HomeView(View):
    template_name = "main/home.html"

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            destinations = user.destination.all()
            interactive_map = folium.Map(location=[0,0], zoom_start=2)
            if destinations is not None:
                for destination in destinations:
                    folium.Marker((destination.latitude, destination.longitude),
                                  popup=destination.country.name + "\n" + destination.city,
                                  icon=folium.Icon()
                                  ).add_to(interactive_map)
            context = {
                "map": interactive_map._repr_html_
            }
        else:
            context = {}
        return render(request, self.template_name, context)
    
def index(request, id):
    message = Message()
    template_name = "todolist/list.html"
    td_list = ToDoList.objects.get(id=id)
    
    if request.method == "POST":
        if request.POST.get("save"):
            for item in td_list.item_set.all():
                item.complete = request.POST.get(f"c{item.id}") == "completed"
                item.to_delete = request.POST.get(f"d{item.id}") == "deleted"
                item.save()
            td_list.item_set.filter(to_delete=True).delete()
        elif request.POST.get("newItem"):
            new_item_text = request.POST.get("new")
            if len(new_item_text) > 2:
                td_list.item_set.create(text=new_item_text, complete=False)
            else:
                message.error(request, "Item name must contain at least 3 character")
    context = {
        'list': td_list,
        'items': td_list.item_set.all(),
    }
    return render(request, template_name, context)      

