from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class EmailModelTests(TestCase):
    def email_with_domain(self):
        email = User()