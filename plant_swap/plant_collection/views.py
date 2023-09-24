from typing import Any
from django.shortcuts import render, redirect, get_list_or_404
from django.views import generic, View
from .models import Plant
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

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