from .models import Plant, Species
from django.db.models import Q, Count
from django.core.cache import cache

def order_query(request, order, context, pagination=None, specie=None, search=None, my_collection=False):
    def slicing(query):
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
        context["pages"] = range(1, objects.filter(species=Species.objects.get(slug=specie)).count() // 12 + 2)
        if 'likes' in order:
            if '-' in order:
                order = order.replace('-','')
                context["plants"] = slicing(objects.filter(species=Species.objects.get(slug=specie)).annotate(likes_count=Count(order)).order_by('-likes_count'))
            else:
                context["plants"] = slicing(objects.filter(species=Species.objects.get(slug=specie)).annotate(likes_count=Count(order)).order_by('likes_count'))
        else:
            context["plants"] = slicing(objects.filter(species=Species.objects.get(slug=specie)).order_by(order))

        # This is for search bar request
    elif request.GET.get("search") or search:
        # This is for search bar request, we are searching for plants that have given string in their nick_name, owner or species name
        plants = search
        if request.GET.get("search"):
            plants=request.GET.get("search")
        context['search'] = plants
        if 'likes' in order:
            if '-' in order:
                order = order.replace('-','')
                context["plants"] = slicing(objects.filter(
                    Q(nick_name__icontains=plants)
                    | Q(owner__username__icontains=plants)
                    | Q(species__name__icontains=plants)
                ).annotate(likes_count=Count(order)).order_by('-likes_count'))
            else:
                context["plants"] = slicing(objects.filter(
                Q(nick_name__icontains=plants)
                | Q(owner__username__icontains=plants)
                | Q(species__name__icontains=plants)
                ).annotate(likes_count=Count(order)).order_by('likes_count'))
        else:
            context["plants"] = slicing(objects.filter(
            Q(nick_name__icontains=plants)
            | Q(owner__username__icontains=plants)
            | Q(species__name__icontains=plants)
            ).order_by(order))
        context["pages"] = range(1, objects.filter(
            Q(nick_name__icontains=plants)
            | Q(owner__username__icontains=plants)
            | Q(species__name__icontains=plants)
            ).count() // 12 + 2)
        
    else:
        if not my_collection:
            context["pages"] = range(1, objects.count() // 12 + 2)
            if 'likes' in order:
                if '-' in order:
                    order = order.replace('-','')
                    context["plants"] = slicing(objects.annotate(likes_count=Count(order)).order_by('-likes_count'))
                else:
                    context["plants"] = slicing(objects.annotate(likes_count=Count(order)).order_by('likes_count'))
            else:
                context["plants"] = slicing(objects.order_by(order))
        else:
            context["pages"] = range(1, (objects.count() + 1) // 12 + 2)
            if 'likes' in order:
                if '-' in order:
                    order = order.replace('-','')
                    context["plants"] = slicing(objects.annotate(likes_count=Count(order)).order_by('-likes_count'))
                else:
                    context["plants"] = slicing(objects.annotate(likes_count=Count(order)).order_by('likes_count'))
            else:
                context["plants"] = slicing(objects.order_by(order))
    return context