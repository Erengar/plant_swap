from django.shortcuts import render, redirect, get_list_or_404
from django.views import generic, View
from django.contrib.auth import login, logout, authenticate
from .models import Plant
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm

# Create your views here.

class personal_collection(LoginRequiredMixin, generic.ListView):
    template_name ='plant_collection/collection.html'
    def get(self, request):
        model = get_list_or_404(Plant, owner=request.user)
        context = {'plants': model}
        return render(request, self.template_name, context)


#Under construction
class front_page(View):
    def get(self, request):
        return render(request, 'base.html', {'form':forms.Form})

class login_view(View):
    template_name = 'login.html'
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
            return redirect('plant_collection:login')

def logout_view(request):
    logout(request)
    return redirect('plant_collection:front_page')