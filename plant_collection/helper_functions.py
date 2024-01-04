from .models import Plant, Species
from django.db.models import Q, Count
from django.core.cache import cache
from django.http import HttpRequest
from django.db.models.query import QuerySet
from pyuploadcare import Uploadcare
from .models import Image

def order_query(request: HttpRequest,
                order: str,
                context: dict[str,str|int],
                pagination: int | None = None,
                specie: str | None =None,
                search: str | None = None,
                my_collection: bool =False) -> dict[str,str|int]:
    def slicing(query: QuerySet):
        if not my_collection:
            slice = query[(context["current_page"] - 1) * 12 : context["current_page"] * 12]
        elif pagination == 1:
            slice = query[(context["current_page"] - 1) * 11: context["current_page"] * 11]
        else:
            slice = query[(context["current_page"] - 1) * 12 - 1 : context["current_page"] * 12 -1]
        return slice
    
    if my_collection:
        objects = Plant.objects.filter(owner=request.user)
    else:
        objects = Plant.objects
    #First we are checking wheter we are receiving request for specific species
    #Order of plants must be case insensitive, but Lower and Count throws error when we are reversing order with '-', therefore we are checking for it
    if specie:
        #If user selected specie that is not by default shown we are unrolling species bar, we use list comprehension just so we do not have to hit the database
        if specie not in [x.slug for x in cache.get('species')]:
            context['species'] = Species.objects.all()
        context['selected_specie'] = specie
        pages = range(1, objects.filter(species=Species.objects.get(slug=specie)).count() // 12 + 2)
        if 'likes' in order:
            if '-' in order:
                order = order.replace('-','')
                objects = objects.filter(species=Species.objects.get(slug=specie)).annotate(likes_count=Count(order)).order_by('-likes_count')
            else:
                objects = objects.filter(species=Species.objects.get(slug=specie)).annotate(likes_count=Count(order)).order_by('likes_count')
        else:
            objects = objects.filter(species=Species.objects.get(slug=specie)).order_by(order)

        # This is for search bar request
    if request.GET.get("search") or search:
        # This is for search bar request, we are searching for plants that have given string in their nick_name, owner or species name
        plants = search
        if request.GET.get("search"):
            plants=request.GET.get("search")
        context['search'] = plants

        pages = range(1, objects.filter(
            Q(nick_name__icontains=plants)
            | Q(owner__username__icontains=plants)
            | Q(species__name__icontains=plants)
            ).count() // 12 + 2)

        if 'likes' in order:
            if '-' in order:
                order = order.replace('-','')
                objects = objects.filter(
                    Q(nick_name__icontains=plants)
                    | Q(owner__username__icontains=plants)
                    | Q(species__name__icontains=plants)
                ).annotate(likes_count=Count(order)).order_by('-likes_count')
            else:
                objects = objects.filter(
                Q(nick_name__icontains=plants)
                | Q(owner__username__icontains=plants)
                | Q(species__name__icontains=plants)
                ).annotate(likes_count=Count(order)).order_by('likes_count')
        else:
            objects = objects.filter(
            Q(nick_name__icontains=plants)
            | Q(owner__username__icontains=plants)
            | Q(species__name__icontains=plants)
            ).order_by(order)
        
    if not specie and not request.GET.get("search") and not search:
        if not my_collection:
            pages = range(1, objects.count() // 12 + 2)
            if 'likes' in order:
                if '-' in order:
                    order = order.replace('-','')
                    objects = objects.annotate(likes_count=Count(order)).order_by('-likes_count')
                else:
                    objects = objects.annotate(likes_count=Count(order)).order_by('likes_count')
            else:
                objects = objects.order_by(order)
        else:
            pages = range(1, (objects.count() + 1) // 12 + 2)
            if 'likes' in order:
                if '-' in order:
                    order = order.replace('-','')
                    objects = objects.annotate(likes_count=Count(order)).order_by('-likes_count')
                else:
                    objects = objects.annotate(likes_count=Count(order)).order_by('likes_count')
            else:
                objects = objects.order_by(order)

                
    context["plants"] = slicing(objects)
    context["pages"] = pages
    return context


def upload_images(pictures: list, plant: Plant) -> None:
    uploadcare = Uploadcare(public_key="f9c7bebe0949bee2838f", secret_key="3d390a60e900c30ee48b")
    for picture in pictures:
        data = pictures[picture]
        ucare_file = uploadcare.upload(data, size=data.size)
        image = Image.objects.create(plant=plant, image=f'https://ucarecdn.com/{ucare_file.uuid}/')
        image.save()