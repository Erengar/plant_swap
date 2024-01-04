from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import add_plant_form, image_form, update_plant_form
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Plant, Species, Image, Thumbnail
from django.views.generic.edit import FormMixin
from django.core.cache import cache
from .helper_functions import order_query, upload_images
from django.http import HttpRequest, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from pyuploadcare import Uploadcare

"""
This view shows all owned plants, defult by number of likes.
"""
class personal_collection(LoginRequiredMixin, generic.View):
    template_name = "plant_collection/collection.html"

    def get(self, request: HttpRequest, pagination: int = 1, order: str ='-likes', search: str | None = None) -> HttpResponse:
        #We cannot order nick_name case insensitively, therefore we are replacing nick_name with slug
        if 'nick_name' in order:
            order = order.replace('nick_name', 'slug')
        context = {}
        context['search'] = search
        context["current_page"] = pagination
        context['order'] = order
        context = order_query(request=request, order=order, context=context, pagination=pagination, search=search, my_collection=True)
        #We still want nick_name to be displayed in url
        if 'slug' in order:
            order = order.replace('slug', 'nick_name')
            context['order'] = order
        return render(request, self.template_name, context)


"""
This view shows all plants depending on selected ordering(default is by likes) and specie selected.
"""
class front_page(generic.View):
    template_name = "front_page.html"

    def get(self, request: HttpRequest,
            pagination: int = 1,
            order: str = '-likes',
            specie: str | None = None,
            search: str | None = None) -> HttpResponse:
        #We cannot order nick_name case insensitively, therefore we are replacing nick_name with slug
        if 'nick_name' in order:
            order = order.replace('nick_name', 'slug')
        context = {}
        context['search'] = search
        #This is here just so we can put active tag on Home tab in navbar when we are rendering from this view
        context['tab_signal'] = 'front_page'
        #Caching is set up for 24 hours, because it is unlikely that new species will be added
        if not cache.get('species'):
            cache.set('species', Species.objects.all()[:34], 60*60*24)
        context['order'] = order
        context["species"] = cache.get('species')
        context["current_page"] = pagination
        context = order_query(request=request, order=order, context=context, specie=specie, search=search)
        #We still want nick_name to be displayed in url
        if 'slug' in order:
            order = order.replace('slug', 'nick_name')
            context['order'] = order
        return render(request, self.template_name, context)


"""
This view is here only to receive species search bar and to unroll species bar on front page.
"""
@method_decorator(csrf_exempt, name="dispatch")
class search(View):
    # This receives get request from search bar
    def get(self, request: HttpRequest, specie: str | None = None) -> HttpResponse:
        #If there is search string in request, we are searching for species that have given string in their name else we are returning all species
        if request.GET.get("search"):
            search = request.GET.get("search")
            species = Species.objects.filter(name__icontains=search.strip())
        else:
            species = Species.objects.all()
        return render(request, "plant_collection/assets/search_species_ajax_response.html", {"species": species, "selected_specie": specie})

'''
This view is for mobile species search, it returns all species
'''
class mobile_specie_search(generic.View):
    template_name = "plant_collection/mobile_specie_search.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        if not cache.get('species_all'):
            cache.set('species_all', Species.objects.all(), 60*60*24)
        species = cache.get('species_all')
        context = {"species": species}
        return render(request, self.template_name, context)


"""
This view shows detailed information about plant. You can also like and delete plants here.
This view receives post reqests for like and delete buttons
"""
class plant_view(generic.View):
    template_name = "plant_collection/plant.html"

    def get(self, request: HttpRequest, slug: str) -> HttpResponse | Http404:
        plant = get_object_or_404(Plant, slug=slug)
        context = {"plant": plant}
        return render(request, self.template_name, context)


    def post(self, request: HttpRequest, slug: str) -> HttpResponse | Http404:
        plant = get_object_or_404(Plant, slug=slug)
        if (image:=(request.POST.get("thumbnail"))) and request.user == plant.owner:
            print(image)
            image = Image.objects.get(pk=image)
            Thumbnail.objects.filter(plant=plant).delete()
            thumbnail = Thumbnail.objects.create(plant=plant, image=image)
            thumbnail.save()
            return redirect("plant_collection:plant_view", slug=slug)
        # If we are not receiving post request for thumbnail, we are receiving post request for delete button
        # we double-check(user that does not own plant should not even see button for deleting)
        # wheter he is owner of plant and if he is we delete it.
        if request.user == plant.owner:
            plant.delete()
        return redirect("plant_collection:personal_collection")


"""
This view is for adding new plant. It is receiving post request only for adding new plant.
"""
class add_plant(LoginRequiredMixin, View):
    template_name = "plant_collection/add_plant.html"
    plant_form = add_plant_form
    ima_form = image_form

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {"form": self.plant_form, "image": self.ima_form}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        plant_form = self.plant_form(request.POST)
        ima_form = self.ima_form(request.FILES)
        # Checks wheter some image was submitted
        # Not great but cant seem to make it work in forms
        if not request.FILES:
            image_error = "You must submit at least one image"
            return render(
                request,
                self.template_name,
                {"form": plant_form, "image": ima_form, "image_error": image_error},
            )
        if plant_form.is_valid() and ima_form.is_valid():
            nick_name = plant_form.cleaned_data["nick_name"]
            owner = User.objects.get(username=request.user.username)
            # Species is not required
            try:
                species = Species.objects.get(name=plant_form.cleaned_data["species"])
            except:
                species = None
            location = plant_form.cleaned_data["location"]
            for_trade = plant_form.cleaned_data["for_trade"]
            content = plant_form.cleaned_data["content"]
            pictures = request.FILES
            # Plant have to be created first
            plant = Plant.objects.create(
                nick_name=nick_name,
                owner=owner,
                species=species,
                location=location,
                for_trade=for_trade,
                content=content
            )
            upload_images(pictures=pictures, plant=plant)
            plant.save()
            return redirect("plant_collection:personal_collection")

        return render(
            request, self.template_name, {"form": plant_form, "image": ima_form}
        )


class update_plant(LoginRequiredMixin, FormMixin,generic.View):
    template_name = "plant_collection/update_plant.html"
    plant_form = update_plant_form
    ima_form = image_form

    # This is for prefilling form with data from database
    def get_initial(self) -> dict:
        plant = get_object_or_404(Plant, slug=self.kwargs["slug"])
        initial = super(update_plant, self).get_initial()
        initial["nick_name"] = plant.nick_name
        initial["species"] = plant.species
        initial["for_trade"] = plant.for_trade
        initial["location"] = plant.location
        initial["content"] = plant.content
        return initial

    def get(self, request: HttpRequest, slug: str) -> HttpResponse | Http404 | HttpResponseRedirect | HttpResponsePermanentRedirect:
        plant = get_object_or_404(Plant, slug=slug)
        # We need to chceck wheter user accessing this url is truly owner of given object.
        # Django permission system is not appropriate and as far as I know there is nothing better than this solution.
        # Userpassestest can be used but it accomplishes the same thing as this.
        if request.user != plant.owner:
            return redirect("plant_collection:front_page")
        form = self.plant_form(initial=self.get_initial())
        image = self.ima_form
        context = {"form": form, "plant": plant, "image": image}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, slug: str) -> HttpResponse | Http404 | HttpResponseRedirect | HttpResponsePermanentRedirect:
        plant = get_object_or_404(Plant, slug=slug)
        # Dont know if this is needed in here, but just to be sure
        if request.user != plant.owner:
            return redirect("plant_collection:front_page")
        form = update_plant_form(request.POST)

        # This conditional is replacing is_valid() function,
        # because is_valid() also calls models validation methods
        # which raise nick_name unique error if nick_name field stays unchanged
        check_unique = plant in Plant.objects.filter(
            nick_name=request.POST["nick_name"]
        ) or not (len(Plant.objects.filter(nick_name=request.POST["nick_name"])) >= 1)
        check_minlength = len(request.POST["nick_name"]) > 3
        if check_unique and check_minlength:
            plant.nick_name = request.POST["nick_name"]
            species = request.POST.get("species", None)
            if species:
                plant.species = Species.objects.get(pk=request.POST["species"])
            else:
                plant.species = None

            trade = request.POST.get("for_trade")
            if trade:
                plant.for_trade = True
            else:
                plant.for_trade = False
            plant.location = request.POST.get("location", None)
            plant.content = request.POST.get("content", None)
            plant.save()

            # This is for deleting images that are in database
            try:
                to_delete = request.POST["to delete"].split(",")
                for image in to_delete:
                    Image.objects.filter(pk=int(image)).delete()
            except:
                pass

            # This is for adding new images, try and for except are for cases when user submits only one image
            pictures = request.FILES
            upload_images(pictures=pictures, plant=plant)

            # This is for deleting plant if there are no images
            if not plant.picture.all():
                plant.delete()
            return redirect("plant_collection:personal_collection")

        context = {"form": form, "plant": plant}
        return render(request, self.template_name, context)
    
def like_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.POST.get('plant'):
        plant = request.POST["plant"]
        user = request.POST["user"]
        p = Plant.objects.get(pk=plant)
        u = User.objects.get(username=user)
        if u in p.likes.all():
            p.likes.remove(u)
        elif u not in p.likes.all():
            p.likes.add(u)
        return HttpResponse(p.number_of_likes())
    return redirect('plant_collection:front_page')