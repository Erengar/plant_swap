from typing import Any
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views import generic, View
from .models import Plant, Species, Image, Trade
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import add_plant_form, image_form, update_plant_form
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Q


'''
This view shows all owned plants by time of adding. You can also like plants here.
This view is receiving post request only for likes
'''
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


'''
This view shows all plants by time of adding. You can also like plants here.
It is receiving 4 kinds of get requests: front page, front page with unrolled species bar, front page with search specified and front page pagination.
This view is recieving post request only for likes.
'''
class front_page(generic.ListView):
    template_name = 'front_page.html'
    model = Plant

    def get(self, request, pagination=1, *args, **kwargs):
        context = {}
        context["species"] = Species.objects.all()[:34]
        context['pages'] = range(1, Plant.objects.count()//12+2)
        context['current_page']=pagination
        context["plants"] = Plant.objects.order_by('-updated')[(context['current_page']-1)*12:context['current_page']*12]
        #This is for search bar request
        try:
            plants = request.GET['search']
            #This is for search bar request, we are searching for plants that have given string in their nick_name, owner or species name
            context["plants"] = Plant.objects.filter(Q(nick_name__icontains=plants) | Q(owner__username__icontains=plants) | Q(species__name__icontains=plants)).order_by('-updated')
        except:
            pass
        return render(request, self.template_name, context)

    def post(self, request):
        #This is for like ajax request
        plant = request.POST['plant']
        user = request.POST['user']
        p = Plant.objects.get(nick_name=plant)
        u = User.objects.get(username=user)  
        if u in p.likes.all():
            p.likes.remove(u)
        elif not u in p.likes.all():
            p.likes.add(u)
        return HttpResponse(p.number_of_likes()) 


'''
This view is here only to receive species search bar and to unroll species bar on front page.
'''
@method_decorator(csrf_exempt, name='dispatch')
class search(View):

    #This receives get request from search bar
    def get(self, request):
        #This should never raise error, but just in case
        try:
            search = request.GET['search'].strip()
        except:
            raise Http404
        species = Species.objects.filter(name__icontains=search)
        response = []
        for specie in species:
            response.append('<li><a href="/species/'+str(specie.slug)+'">'+specie.name+'</a></li>')
        return HttpResponse("".join(response)+'</ul>')
    
    #This receives patch request from unroll species bar
    def patch(self, request):
        species = Species.objects.all()
        response = []
        for specie in species:
            response.append('<li><a href="/species/'+str(specie.slug)+'">'+specie.name+'</a></li>')
        return HttpResponse("".join(response)+'</ul>')


'''
This view shows all plants of given species. You can also like plants here.
'''
class species_list_view(generic.ListView):
    template_name = 'plant_collection/species.html'
    model = Plant
    #This display all plants of given species, slug of specie is passed under 'nam' variable
    def get(self, request, nam):
        species = get_object_or_404(Species, slug=nam)
        plants = Plant.objects.filter(species=species)
        species = Species.objects.all()
        context = {'species':species,
                   'plants':plants}
        return render(request, self.template_name, context)
    
    #This is for like ajax request
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
    

'''
This view shows detailed information about plant. You can also like and delete plants here.
This view receives post reqests for like and delete buttons
'''
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
    wheter our plant slug is in that url. If it comes through this we know it is 'like' request, otherwise it is 'delete' request.
    '''
    def post(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        try_url = request.POST.get('url')
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
        #If user is not liking plant, he is deleting it, 
        #we double-check(user that does not own plant should not even see button for deleting)
        #wheter he is owner of plant and if he is we delete it.
        elif request.user == plant.owner:
            plant.delete()
        return redirect('plant_collection:personal_collection')
        
    
'''
This view is for adding new plant. It is receiving post request only for adding new plant.
'''
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
        #Checks wheter some image was submitted
        #Not great but cant seem to make it work in forms
        if not request.FILES:
            image_error = 'You must submit at least one image'
            return render(request, self.template_name, {'form':plant_form, 'image':ima_form, 'image_error':image_error})
        if plant_form.is_valid() and ima_form.is_valid():
            nick_name = request.POST['nick_name']
            owner = User.objects.get(username=request.user.username)
            #Species is not required
            try:
                species = Species.objects.get(pk=request.POST['species'])
            except:
                species = None
            pictures = request.FILES
            #Plant have to be created first
            plant = Plant.objects.create(nick_name=nick_name,
                                         owner=owner,
                                         species=species)
            #We are using try for cases if user submits more than 1 picture
            try:
                plant.save()
                for picture in pictures:
                    image = Image.objects.create(plant=plant, image=pictures[picture])
                    image.save()
            #If only one picture is submitted, it is not iterable and handled by except
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
    
    def get(self,request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        #We need to chceck wheter user accessing this url is truly owner of given object. 
        #Django permission system is not appropriate and as far as I know there is nothing better than this solution.
        #Userpassestest can be used but it accomplishes the same thing as this.
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
        #Dont know if this is needed in here, but just to be sure
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
            species = request.POST.get('species', None)
            if species:
                plant.species = Species.objects.get(pk=request.POST['species'])
            else:
                plant.species = None

            trade = request.POST.get('for_trade')
            if trade:
                plant.for_trade = True
            else:
                plant.for_trade = False
            plant.save()

            #This is for deleting images that are in databse
            try:
                to_delete = request.POST['to delete'].split(',')
                for image in to_delete:
                    Image.objects.filter(pk=int(image)).delete()
            except:
                pass

            #This is for adding new images, try and for except are for cases when user submits only one image
            pictures = request.FILES
            try:
                for picture in pictures:
                    image = Image.objects.create(plant=plant, image=pictures[picture])
                    image.save()
            except:
                image = Image.objects.create(plant=plant, image=pictures['image'])
                image.save()
            
            #This is for deleting plant if there are no images
            if not plant.picture.all():
                plant.delete()
            return redirect('plant_collection:personal_collection')
            
        context = {'form':form,
                   'plant':plant}
        return render(request, self.template_name, context)
    
    

'''
This view is for making trade between two plants.
It is receiving two kinds of get requests: one for ajax request for user requesting trade and one for displaying desired plant.
'''
class trade(LoginRequiredMixin, View):
    def get(self, request, req,*args, **kwargs):
        #This is for ajax request to return plant that user selected as to be traded
        try:
            plant = get_object_or_404(Plant, nick_name=request.GET['plant'].strip())
            return render(request, 'plant_collection/trade_offered_plant.html', {'plant':plant})
        except:
            pass
        req_plant = get_object_or_404(Plant, slug=req)
        return render(request, 'plant_collection/trade.html', {'req':req_plant})
    
    #Two plants are posted and trade is made between their owners
    def post(self, request, *args, **kwargs):
        offered = get_object_or_404(Plant, nick_name=request.POST['offered'])
        requested = get_object_or_404(Plant, nick_name=request.POST['requested'])
        initiator = request.user
        recipient = requested.owner
        errors = []
        #Checking wheter user is not trying to trade with himself, wheter he has not already made this trade
        if offered.owner == recipient:
            errors.append('You cannot trade with yourself.')
        if Trade.objects.filter(plant_offered=offered, plant_requested=requested, initiator=initiator, recipient=recipient):
            errors.append('You have already made this trade.')
        if errors:
            return render(request, 'plant_collection/trade.html', {'req':requested, 'errors':errors})
        trade = Trade.objects.create(plant_offered=offered, plant_requested=requested, initiator=initiator, recipient=recipient)
        trade.save()
        return redirect('plant_collection:personal_collection')
    
'''
This view is for displaying all trades that given plant is involved in.
'''
class plant_offers(LoginRequiredMixin, generic.ListView):
    template_name = 'plant_collection/plant_offers.html'
    model = Trade
    def get(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        if request.user ==plant.owner:
            #Showing only trades that are not finalized
            req = Trade.objects.filter(plant_requested=plant, finalized=False)
            offered = Trade.objects.filter(plant_offered=plant, finalized=False)
            context = {'offers':offered, 'requests':req, 'plant':plant}
            return render(request, self.template_name, context)
        else:
            return redirect('plant_collection:front_page')