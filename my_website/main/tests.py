from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from main.models import ToDoList, Item
from main.forms import CreateNewList

# Create your tests here.
class ToDoListTest(TestCase):

    def create_user(self, username='testuser', password='12345'):
        return User.objects.create_user(username=username, password=password)
    
    def create_todo_list(self, name='Only a test'):
        user = self.create_user()
        return ToDoList.objects.create(user=user, name=name)
    
    def test_todo_list_creation(self):
        todolist = self.create_todo_list()
        self.assertTrue(isinstance(todolist, ToDoList))
        self.assertEqual(todolist.__str__(), todolist.name)

class ItemTest(ToDoListTest, TestCase):

    def create_item(self, text='Only a test'):
        todolist = self.create_todo_list()
        return Item.objects.create(todolist=todolist, 
                                   text=text,
                                   complete=False,
                                   to_delete=False)
    
    def test_item_creation(self):
        item = self.create_item()
        self.assertTrue(isinstance(item, Item))
        self.assertEqual(item.__str__(), item.text)