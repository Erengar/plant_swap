from typing import Any
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import generic, View
from .models import Plant, Species, Image
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import add_plant_form, image_form, update_plant_form
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator

#This view is receiving post request only for likes
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


#This view is recieving post request only for likes
class front_page(generic.ListView):
    template_name = 'front_page.html'
    model = Plant

    def get(self, request):
        context = {}
        context["plants"] = Plant.objects.order_by('-updated')
        context["species"] = Species.objects.all()[:20]
        try:
            plants = request.GET['search']
            context["plants"] = Plant.objects.filter(nick_name__icontains=plants).order_by('-updated')
        except:
            pass
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

#This view receives post reqests for like and delete buttons
class plant_view(generic.DetailView):
    template_name = 'plant_collection/plant.html'
    model = Plant
    def get(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        context = {'plant': plant}
        return render(request, self.template_name, context)
    
    '''
    Both delete and like button-on-plant-view are POSTing on plant_view, thus it is necessary to provide some logic what to execute when.
    When user likes the picture Ajax sends its url as context then we simply check wheter there is 'url' context, and if there is
    wheter our plant slug is in that url. If it comes through this we know it is 'like' request, otherwise it is 'delete' request.'''
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
    

class update_plant(LoginRequiredMixin, generic.UpdateView):
    template_name = 'plant_collection/update_plant.html'
    model = Plant
    plant_form = update_plant_form
    ima_form = image_form

    def test_func(self,slug) -> bool | None:
        plant = get_object_or_404(Plant, slug=slug)
        return self.request.user == plant.owner
    
    def get(self,request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        #We need to chceck wheter user accessing this url is truly owner of given object. 
        #Django permission system is not appropriate and as far as I know there is nothing better than this solution.
        if request.user != plant.owner:
            return redirect('plant_collection:front_page')
        form = self.plant_form(instance=plant)
        image = self.ima_form
        context = {'form':form,
                   'plant':plant,
                   'image':image}
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        #Dont know if this is needed it here
        if request.user != plant.owner:
            return redirect('plant_collection:front_page')
        form = update_plant_form(request.POST)

        #This conditional is replacing is_valid() function,
        #because is_valid() also calls models validation methods
        # which raise nick_name unique error if nick_name field stays unchanged
        check_unique = plant in Plant.objects.filter(nick_name=request.POST['nick_name']) or not (len(Plant.objects.filter(nick_name=request.POST['nick_name']))>=1)
        check_minlength = (len(request.POST['nick_name'])>3)
        if check_unique and check_minlength:
            plant.nick_name = request.POST['nick_name']
            try:
                plant.species = Species.objects.get(pk=request.POST['species'])
            except:
                plant.species = None
            try:
                request.POST['for_trade']
                plant.for_trade = True
            except:
                plant.for_trade = False
            plant.save()

            try:
                to_delete = request.POST['to delete'].split(',')
                for image in to_delete:
                    Image.objects.filter(pk=int(image)).delete()
            except:
                pass

            pictures = request.FILES
            try:
                for picture in pictures:
                    image = Image.objects.create(plant=plant, image=pictures[picture])
                    image.save()
            except:
                image = Image.objects.create(plant=plant, image=pictures['image'])
                image.save()
            if not plant.picture.all():
                plant.delete()
            return redirect('plant_collection:personal_collection')
            
        context = {'form':form,
                   'plant':plant}
        return render(request, self.template_name, context)
    

#This view receives post request only for likes
class species_list_view(generic.ListView):
    template_name = 'plant_collection/species.html'
    model = Plant
    def get(self, request, nam):
        species = get_object_or_404(Species, slug=nam)
        plants = Plant.objects.filter(species=species)
        species = Species.objects.all()
        context = {'species':species,
                   'plants':plants}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        plant = request.POST['plant']
        user = request.POST['user']
        p = Plant.objects.get(nick_name=plant)
        u = User.objects.get(username=user)  
        if u in p.likes.all():
            p.likes.remove(u)
        elif not u in p.likes.all():
            p.likes.add(u)
        return HttpResponse(p.number_of_likes())
    

#This view receives requests only from species search bar
@method_decorator(csrf_exempt, name='dispatch')
class search(View):

    @csrf_protect
    def get(self, request):
        search = request.GET['search']
        species = Species.objects.filter(name__icontains=search)
        response = []
        for specie in species:
            response.append('<li><a href="/species/'+str(specie.slug)+'">'+specie.name+'</a></li>')
        return HttpResponse("".join(response)+'</ul>')
    
    def patch(self, request):
        print(request)
        species = Species.objects.all()
        response = []
        for specie in species:
            response.append('<li><a href="/species/'+str(specie.slug)+'">'+specie.name+'</a></li>')
        return HttpResponse("".join(response)+'</ul>')