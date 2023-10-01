from typing import Any
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import generic, View
from .models import Plant, Species, Image
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import add_plant_form, image_form
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.http import HttpResponse


class personal_collection(LoginRequiredMixin, generic.ListView):
    template_name ='plant_collection/collection.html'
    def get(self, request):
        model = Plant.objects.filter(owner=request.user).order_by('-updated')
        context = {'plants': model}
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        plant = request.POST['plant']
        user = request.POST['user']
        p = Plant.objects.get(nick_name=plant)
        u = User.objects.get(username=user)
        if u in p.likes.all():
            p.likes.remove(u)
        elif not u in p.likes.all():
            p.likes.add(u)
        return HttpResponse(p.number_of_likes())


#Under construction
class front_page(generic.ListView):
    template_name = 'front_page.html'
    model = Plant
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["plants"] = Plant.objects.order_by('-updated')
        return context

    def post(self, request):
        plant = request.POST['plant']
        user = request.POST['user']
        p = Plant.objects.get(nick_name=plant)
        u = User.objects.get(username=user)  
        if u in p.likes.all():
            p.likes.remove(u)
        elif not u in p.likes.all():
            p.likes.add(u)
        return HttpResponse(p.number_of_likes())

class plant_view(generic.DetailView):
    template_name = 'plant_collection/plant.html'
    model = Plant
    def get(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        context = {'plant': plant}
        return render(request, self.template_name, context)
    
    '''
    Both delete and like button-on-plant-view are POSTing on plant_view, thus it is necessary to provide some logic what to execute when.
    When we user likes the picture like Ajax sends its url as context then we simply check wheter there is 'url' context, and if there is
    wheter our plant slug is in that url. If it comes through this we know it is like request, otherwise it is delete request.'''
    def post(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        try_url = 'č'
        try:
            try_url = request.POST['url']
        except:
            pass
        if plant.slug in try_url:
            plant = request.POST['plant']
            user = request.POST['user']
            p = Plant.objects.get(nick_name=plant)
            u = User.objects.get(username=user)  
            if u in p.likes.all():
                p.likes.remove(u)
            elif not u in p.likes.all():
                p.likes.add(u)
            return HttpResponse(p.number_of_likes())
        elif request.user == plant.owner:
            plant.delete()
        return redirect('plant_collection:personal_collection')
        
    

class add_plant(LoginRequiredMixin, View):
    template_name= 'plant_collection/add_plant.html'
    plant_form = add_plant_form
    ima_form = image_form
    def get(self,request):
        context = {'form':self.plant_form, 'image':self.ima_form}
        return render(request, self.template_name, context)
        
    def post(self,request):
        plant_form = add_plant_form(request.POST)
        ima_form = image_form(request.FILES)
        #Not great but cant seem to make it work in forms
        if not request.FILES:
            image_error = 'You must submit at least one image'
            return render(request, self.template_name, {'form':plant_form, 'image':ima_form, 'image_error':image_error})
        if plant_form.is_valid() and ima_form.is_valid():
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
            try:
                plant.save()
                for picture in pictures:
                    image = Image.objects.create(plant=plant, image=pictures[picture])
                    image.save()
            except:
                image = Image.objects.create(plant=plant, image=pictures['picture0'])
                image.save()
                plant.save()
            return redirect('plant_collection:personal_collection')
        
        return render(request, self.template_name, {'form':plant_form, 'image':ima_form})
    

class update_plant(generic.UpdateView, UserPassesTestMixin):
    template_name = 'plant_collection/update_plant.html'
    model = Plant
    form_class = add_plant_form
    def get(self,request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        form = self.form_class()
        context = {'form':form,
                   'plant':plant}
        return render(request, self.template_name, context)