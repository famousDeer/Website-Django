from django.test import TestCase
from django.contrib.auth.models import User

from main.models import ToDoList, Item
from main.forms import CreateNewList

# Testing models.
class TestAppModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        testuser = User.objects.create_user(username='testuser', password='12345')
        testuser2 = User.objects.create_user(username='testuser2', password='123456')
        cls.todolist = ToDoList.objects.create(user_id=testuser.id, name='Only a test')
        cls.todolist2 = ToDoList.objects.create(user_id=testuser2.id, name='Test2')
        cls.item = Item.objects.create(todolist=cls.todolist, 
                                   text='Only a test',
                                   complete=False,
                                   to_delete=False)
        cls.item2 = Item.objects.create(todolist=cls.todolist2, 
                                   text='Test2',
                                   complete=False,
                                   to_delete=False)
    
    def test_todo_list_creation(self):
        self.assertTrue(isinstance(self.todolist, ToDoList))
        self.assertEqual(self.todolist.__str__(), 'Only a test')

    def test_item_creation(self):
        self.assertTrue(isinstance(self.item, Item))
        self.assertEqual(self.item.__str__(), 'Only a test')

    def test_item_user(self):
        self.assertEqual(self.item.text, 'Only a test')

    def test_item_user2(self):
        self.assertEqual(self.item2.text, 'Test2')
    
