from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from main.views import index, HomeView, ToDoListView
from main.models import ToDoList, Item

# Testing views.

class TestViewTemplateResolves(TestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomeView)
        
    
    def test_view_url_resolves(self):
        url = reverse('view')
        self.assertEqual(resolve(url).func.view_class, ToDoListView)

class TestViews(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.testuser = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.view_url = reverse('view')
        self.home_url = reverse('home')
        self.delete_url = reverse('delete', args=[1])

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_todolist_POST_create_new_list(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.view_url, {'name': 'First List'})
        self.assertEqual(response.status_code, 302)
    
    def test_todolist_POST_create_new_list_no_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.testuser.todolist.count(), 0)


