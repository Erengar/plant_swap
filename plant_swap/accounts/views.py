from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.views import generic, View

# Create your views here.


class login_view(View):
    template_name = 'accounts/login.html'
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})

    #Dont know about safety here, additional work required
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('plant_collection:personal_collection')
        else:
            return redirect('accounts:login')
        

def logout_view(request):
    logout(request)
    return redirect('plant_collection:front_page')

class registration_view(View):
    template_name = 'accounts/registration.html'
    def get(self, request):
        form = RegistrationForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    #No idea how save this is
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        form =RegistrationForm(request.POST)
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