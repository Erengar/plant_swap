from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth import login
from .models import Plant
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class personal_collection(LoginRequiredMixin, generic.ListView):
    template_name ='plant_collection/collection.html'
    def get(self, request):
        model = {'plants': Plant.objects.filter(owner=request.user)}
        return render(request, self.template_name, model)

class front_page(View):
    def get(request):
        render(request, 'plant_collection/login', {'form':forms.Form})