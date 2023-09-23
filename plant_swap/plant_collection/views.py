from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_list_or_404
from django.views import generic, View
from django.contrib.auth import login, logout, authenticate
from .models import Plant
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User

# Create your views here.

class personal_collection(LoginRequiredMixin, generic.ListView):
    template_name ='plant_collection/collection.html'
    def get(self, request):
        model = Plant.objects.filter(owner=request.user)
        context = {'plants': model}
        return render(request, self.template_name, context)


#Under construction
'''
class front_page(View):
    template_name = 'front_page.html'
    def get(self, request):
        plants = Plant.objects.order_by('updated')
        context = {'plants':plants}
        return render(request, self.template_name, context)
'''
class front_page(generic.ListView):
    template_name = 'front_page.html'
    model = Plant
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["plants"] = Plant.objects.order_by('updated')
        return context
    

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

class registration_view(View):
    template_name = 'registration.html'
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
        if password != confirm_password:
            return redirect('plant_collection:registration')
        c = User.objects.create_user(username=username,
                                    password=password,
                                    email=email)
        c.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('plant_collection:front_page')
        return redirect('plant_collection:front_page')