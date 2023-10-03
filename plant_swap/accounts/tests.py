from django.test import TestCase, Client
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm

#Check error messages
class test_login(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(username='Polo', password='Liteon987')

    def test_login_pass(self):
        log =self.client.login(username='Polo', password='Liteon987')
        return self.assertEqual(log, True)

    def test_login_notpass(self):
        log = self.client.login(username='test', password='test')
        return self.assertEqual(log, False)
    
    def get_login_submit(self):
        page = self.client.get('/accounts/login/').content.decode('utf-8')
        return self.assertInHTML('<input class="button" type="submit" value="Submit">', page)
    
    def get_login_navbar(self):
        page = self.client.get('/accounts/login/').content.decode('utf-8')
        return self.assertInHTML("<nav class='navbar' role='navigation' style='position:sticky !important'>", page)
    
    def test_login_redirect(self):
        self.client.login(username='Polo', password='Liteon987')
        response = self.client.get('/accounts/login/')
        return self.assertRedirects(response, '/my-collection/')

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        return self.assertTemplateUsed(response, 'accounts/login.html')

class test_registration(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(username='Polo', password='Liteon987', email='test@test')

    def test_registration_submit(self):
        page = self.client.get('/accounts/registration/').content.decode('utf-8')
        return self.assertInHTML('<input class="button" type="submit" value="Submit">', page)
    
    def test_registration_navbar(self):
        page = self.client.get('/accounts/registration/')
        return self.assertContains(page, "<nav class='navbar' role='navigation' style='position:sticky !important'>")
    def test_registration_redirect(self):
        self.client.login(username='Polo', password='Liteon987')
        response = self.client.get('/accounts/registration/')
        return self.assertRedirects(response, '/my-collection/')

    def test_registration_unique_username(self):
        page = self.client.post('/accounts/registration/', {'username': 'Polo', 'email':'test@test','password': 'test', 'confirm_password': 'test'}).content.decode('utf-8')
        return self.assertInHTML('Username already taken.' ,page)
    
    def test_registration_unique_email(self):
        page = self.client.post('/accounts/registration/', {'username': 'test', 'email':'test@test','password': 'test', 'confirm_password': 'test'}).content.decode('utf-8')
        return self.assertInHTML('Email adress is already taken.' ,page)
    
    def test_registration_valid_email(self):
        page = self.client.post('/accounts/registration/', {'username': 'test', 'email':'test@test','password': 'test', 'confirm_password': 'test'}).content.decode('utf-8')
        return self.assertInHTML('Enter a valid email address.' ,page)

    def test_registration_length_password(self):
        page = self.client.post('/accounts/registration/', {'username': 'test', 'email':'test@test','password': 'test', 'confirm_password': 'test'}).content.decode('utf-8')
        return self.assertInHTML('Ensure this value has at least 9 characters (it has 4).' ,page)
    
    def test_registration_password_match(self):
        page = self.client.post('/accounts/registration/', {'username': 'test', 'email':'test@test','password': 'test', 'confirm_password': 'test1'}).content.decode('utf-8')
        return self.assertInHTML('Password and Confirm password do not match!' ,page)
    
    def test_registration_upper_lower_password(self):
        page = self.client.post('/accounts/registration/', {'username': 'test', 'email':'test@test','password': 'test', 'confirm_password': 'test'}).content.decode('utf-8')
        return self.assertInHTML('Password must contain at least one uppercase letter and one lowercase letter.' ,page)
    
    def test_registration_numbers_letters_password(self):
        page = self.client.post('/accounts/registration/', {'username': 'test', 'email':'test@test','password': 'test', 'confirm_password': 'test'}).content.decode('utf-8')
        return self.assertInHTML('Password must contain letters and numbers.' ,page)
    
    def test_registration_success(self):
        pass

    def test_registration_view(self):
        response = self.client.get('/accounts/registration/')
        return self.assertTemplateUsed(response, 'accounts/registration.html')

    def form(self):
        form = RegistrationForm
        field_name = 'email'
        with self.subTest(input_value='test@test'):
            form = RegistrationForm({field_name: 'test@test'})
            return self.assertFormError(form, field_name, 'test@test', 'erengagr3@gmail.com')