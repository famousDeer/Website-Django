from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import ToDoList
from .forms import CreateNewList

# Create your views here.

def delete(request, id):
    tdTable = ToDoList.objects.get(id=id)
    messages.info(request, f"Successfully deleted {tdTable.name}")
    tdTable.delete()
    return redirect(reverse('view'))

def home(request):
    return render(request, "main/home.html", {})

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

def todolist(request):
    ls = request.user.todolist.all().count()
    return render(request, "main/todolist.html", {"ls":ls})

def view(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)
        
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(request, "main/view.html", {"form":form})
