from django.test import TestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver

# Create your tests here.

class PlantModelTest(TestCase):
    def single_image(self):
        c = Client()
        milky = open('C:\Users\Adam\Desktop\milky.jpg', 'r')
        respnse = c.post('/my-collection/add-plant/', {'nick_name': 'Plant',
                                                    'picture': milky})
        self.assertContains(respnse, milky, True)