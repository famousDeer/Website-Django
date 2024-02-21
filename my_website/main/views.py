from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_protect

from .models import ToDoList
from .forms import CreateNewList

# Create your views here.

class ToDoListView(View):
    template_name = "main/view.html"

    def get(self, request):
        form = CreateNewList()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = CreateNewList(request.POST)
        delete_id = request.POST.get("delete_id")
        
        if form.is_valid():
            name = form.cleaned_data["name"]
            todolist = ToDoList(name=name)
            todolist.save()
            request.user.todolist.add(todolist)

            return redirect("/%i" %todolist.id)
        elif delete_id:
            tdTable = ToDoList.objects.get(id=delete_id)
            messages.info(request, f"Successfully deleted {tdTable.name}")
            tdTable.delete()

        return redirect('view')

class HomeView(View):
    template_name = "main/home.html"

    def get(self, request):
        return render(request, self.template_name)
    
def index(request, id):
    ls = ToDoList.objects.get(id=id)

    if request.method == "POST":
        if request.POST.get("save"):
            for item in ls.item_set.all():
                if request.POST.get(f"c{item.id}") == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                
                if request.POST.get(f"d{item.id}") == "deleted":
                    item.to_delete = True
                else:
                    item.to_delete = False

                item.save()
                
            ls.item_set.filter(to_delete=True).delete()
        
        elif request.POST.get("newItem"):
            text = request.POST.get("new")
            if len(text) > 2:
                ls.item_set.create(text=text, complete=False)
            else:
                messages.error(request, "Item name must contain at least 3 character")

    return render(request, "main/list.html", {"ls":ls})

