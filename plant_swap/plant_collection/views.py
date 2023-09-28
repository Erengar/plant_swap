from typing import Any
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import generic, View
from .models import Plant, Species, Image
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import add_plant_form
from django.core.files.storage import default_storage
from django.contrib.auth.models import User


import sys

sys.path.append('../accounts')

from accounts.forms import LoginForm, RegistrationForm

# Create your views here.

class personal_collection(LoginRequiredMixin, generic.ListView):
    template_name ='plant_collection/collection.html'
    def get(self, request):
        model = Plant.objects.filter(owner=request.user).order_by('-updated')
        context = {'plants': model}
        return render(request, self.template_name, context)


#Under construction
class front_page(generic.ListView):
    template_name = 'front_page.html'
    model = Plant
    login_form = LoginForm()
    registration_form = RegistrationForm()
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["plants"] = Plant.objects.order_by('-updated')
        return context
    
class plant_view(generic.DetailView):
    template_name = 'plant_collection/plant.html'
    model = Plant
    def get(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        context = {'plant': plant}
        return render(request, self.template_name, context)
    

class add_plant(LoginRequiredMixin, View):
    template_name= 'plant_collection/add_plant.html'
    form_class = add_plant_form
    def get(self,request):
        form = self.form_class()
        context = {'form':form}
        return render(request, self.template_name, context)
        
    def post(self,request):
        form = add_plant_form(request.POST)
        if form.is_valid():
            nick_name = request.POST['nick_name']
            owner = User.objects.get(username=request.user.username)
            try:
                species = Species.objects.get(pk=request.POST['species'])
            except:
                species = None
            pictures = request.FILES
            plant = Plant.objects.create(nick_name=nick_name,
                                         owner=owner,
                                         species=species)
            print(pictures)
            '''
            try:
                image = Image.objects.create(plant=plant, image=pictures)
                image.save()
                plant.save()
            except:
                plant.save()
                for picture in pictures:
                    image = Image.objects.create(plant=plant, image=picture)
                    image.save()
            '''
            return redirect('plant_collection:personal_collection')
        
        return render(request, self.template_name, {'form':form})