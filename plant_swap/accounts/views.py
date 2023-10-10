from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from plant_collection.models import Trade
from django.http import Http404, HttpResponse

# Create your views here.

class login_view(LoginView):
    template_name = 'accounts/login.html'
    next_page = ('plant_collection:personal_collection')
    authentication_form = LoginForm
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    return redirect('plant_collection:front_page')

class registration_view(View):
    template_name = 'accounts/registration.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('plant_collection:personal_collection')
        form = RegistrationForm
        context = {'form':form}
        return render(request, self.template_name, context)


    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        form = RegistrationForm(request.POST)
        if form.is_valid():
            c = User.objects.create_user(username=username,
                                        password=password,
                                        email=email)
            c.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('plant_collection:front_page')
        return render(request, self.template_name, {'form':form})
    
class trades_view(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/offers.html'
    model = Trade
    def get(self, request):
        req = Trade.objects.filter(recipient=request.user)
        offered = Trade.objects.filter(initiator=request.user)
        context = {'offers':offered, 'requests':req}
        return render(request, self.template_name, context)
    

#This view accepts ajax post request for confirming a trade
class trade_view(LoginRequiredMixin, generic.DetailView):
    template_name = 'accounts/trade.html'
    model = Trade

    def get(self, request, pk):
        trade = get_object_or_404(Trade, pk=pk)
        context = {'trade':trade}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        trade = get_object_or_404(Trade, plant_offered=request.POST['offerer'], plant_requested=request.POST['requester'])
        print('here')
        if request.POST['finalize'] and request.user.username == trade.initiator:
            trade.offered_finalized = True
            trade.save()
            return HttpResponse('<i class="fa-solid fa-circle-check is-size-1 gree-check sendable"></i>')
        elif request.POST['finalize'] and request.user.username == trade.recipient:
            trade.requested_finalized = True
            trade.save()
            return HttpResponse('<i class="fa-solid fa-circle-check is-size-1 green-check sendable"></i>')
        elif not request.POST['finalize'] and request.user.username == trade.initiator:
            trade.offered_finalized = False
            trade.save()
            return HttpResponse('<i class="fa-solid fa-circle-check is-size-1 red-check sendable"></i>')
        elif not request.POST['finalize'] and request.user.username == trade.recipient:
            trade.requested_finalized = False
            trade.save()
            return HttpResponse('<i class="fa-solid fa-circle-check is-size-1 red-check sendable"></i>')
        else:
            raise Http404("You are not authorized to do that")