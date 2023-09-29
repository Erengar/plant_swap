from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.views import generic, View
from django.contrib.auth.views import LoginView

# Create your views here.

class login_view(LoginView):
    template_name = 'accounts/login.html'
    next_page = ('plant_collection:personal_collection')
    authentication_form = LoginForm
    redirect_authenticated_user = True

'''OBSOLETE
class logina_view(View):
    template_name = 'accounts/login.html'
    form = LoginForm()

    def get(self, request):
        return render(request, self.template_name, {'form':self.form})

    #Dont know about safety here
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('plant_collection:personal_collection')
        else:
            return render(request, self.template_name, {'form': self.form})
'''

def logout_view(request):
    logout(request)
    return redirect('plant_collection:front_page')

class registration_view(View):
    template_name = 'accounts/registration.html'

    def get(self, request):
        form = RegistrationForm
        context = {'form':form}
        return render(request, self.template_name, context)


    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        form = RegistrationForm(request.POST)
        if form.is_valid():
            c = User.objects.create_user(username=username,
                                        password=password,
                                        email=email)
            c.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('plant_collection:front_page')
        return render(request, self.template_name, {'form':form})