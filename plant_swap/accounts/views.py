from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm, RegistrationForm, MessageForm
from django.contrib.auth.models import User
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from plant_collection.models import Trade, Plant
from django.http import Http404, HttpResponse
from .models import Message

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
        #Show all trades that are not finalized
        req = Trade.objects.filter(recipient=request.user, finalized=False)
        offered = Trade.objects.filter(initiator=request.user, finalized=False)
        context = {'offers':offered, 'requests':req}
        return render(request, self.template_name, context)
    

'''
This view is for showing the trade details and finalizing the trade.
It receives 2 kinds of POST requests: One for accepting/declining/retracting a trade, and the other for finalizing a trade.
'''
class trade_view(LoginRequiredMixin, generic.DetailView):
    template_name = 'accounts/trade.html'
    model = Trade

    def get(self, request, pk):
        trade = get_object_or_404(Trade, pk=pk)
        context = {'trade':trade}
        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        #This part is for accepting or declining a trade
        decline = request.POST.get('decline', None)
        accept = request.POST.get('accept', None)
        retract = request.POST.get('retract', None)
        if decline:
            request.POST['decline']
            trade = get_object_or_404(Trade, pk=pk)
            trade.decline()
            req = Trade.objects.filter(recipient=request.user, finalized=False)
            offered = Trade.objects.filter(initiator=request.user, finalized=False)
            confirm = 'Trade offer was declined.'
            context = {'offers':offered, 'requests':req, 'confirmations': confirm}
            return render(request, 'accounts/offers.html', context)
        if accept:
            request.POST['accept']
            trade = get_object_or_404(Trade, pk=pk)
            trade.accept()
            req = Trade.objects.filter(recipient=request.user, finalized=False)
            offered = Trade.objects.filter(initiator=request.user, finalized=False)
            confirm = 'Trade offer was accepted.'
            context = {'offers':offered, 'requests':req, 'confirmations': confirm}
            return render(request, 'accounts/offers.html', context)
        if retract:
            request.POST['retract']
            trade = get_object_or_404(Trade, pk=pk)
            trade.decline()
            req = Trade.objects.filter(recipient=request.user, finalized=False)
            offered = Trade.objects.filter(initiator=request.user, finalized=False)
            confirm = 'Trade offer was retracted.'
            context = {'offers':offered, 'requests':req, 'confirmations': confirm}
            return render(request, 'accounts/offers.html', context)


        #This part is for finalizing a trade
        offerer = get_object_or_404(Plant, nick_name=request.POST['offerer'])
        requester = get_object_or_404(Plant, nick_name=request.POST['requester'])
        trade = get_object_or_404(Trade, plant_offered=offerer, plant_requested=requester)
        #For some reason request.POST['finalize'] is string even though it should have been boolean, therefore it must be converted to boolean
        if request.POST['finalize'] == 'true':
            finalize = True
        elif request.POST['finalize'] == 'false':
            finalize = False

        #Finalize trade if both parties have finalized
        if finalize and request.user.username == str(trade.initiator) and trade.requested_finalized:
            trade.finalized = True
            trade.save()
            trade.exchange()
        elif finalize and request.user.username == str(trade.recipient) and trade.offered_finalized:
            trade.finalized = True
            trade.save()
            trade.exchange()

        #Update trade status
        #trade.initiator/recipient returns django model object, thus it must be first converted to string before comparison
        if finalize and request.user.username == str(trade.initiator):
            trade.offered_finalized = True
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 green-check sendable")
        elif finalize and request.user.username == str(trade.recipient):
            trade.requested_finalized = True
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 green-check sendable")
        elif not finalize and request.user.username == str(trade.initiator):
            trade.offered_finalized = False
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 red-check sendable")
        elif not finalize and request.user.username == str(trade.recipient):
            trade.requested_finalized = False
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 red-check sendable")
        else:
            raise Http404("You are not authorized to do that")
        

'''
This view is for showing plants user have liked. It receives a POST request when user clicks like button.
'''
class liked_list(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/like_list.html'
    model = Plant
    def get(self, request):
        context = {'plants':Plant.objects.filter(likes=request.user).order_by('-updated')}
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
This receives receives GET and POST requests. It show all messages and allows delete of messages.
'''
class messages_view(LoginRequiredMixin, generic.ListView):
    def get(self, request):
        messages = Message.objects.filter(receiver=request.user).order_by('-date_sent')
        context = {'messages':messages}
        return render(request, 'accounts/messages.html', context)
    
    def post(self, request):
        for req in request.POST:
            if req != 'csrfmiddlewaretoken':
                m = Message.objects.get(slug_subject=req)
                m.delete()
        return redirect('accounts:messages')

'''
This receives only GET request, but need additional parameter for identifying message to display.
It is for showing the message. It also marks the message as read.
'''
class message_view(LoginRequiredMixin, generic.DetailView):
    def get(self, request, slug):
        message = get_object_or_404(Message, slug_subject=slug)
        if request.user != message.receiver and request.user != message.sender:
            raise Http404("You are not authorized to do that")
        message.read = True
        message.save()
        context = {'message':message}
        return render(request, 'accounts/message.html', context)



'''
This view receives both GET and POST requests. It is for writing a message. It is utilizing django forms.
'''
class write_message_view(LoginRequiredMixin, generic.CreateView):
    def get(self, request):
        form = MessageForm
        context = {'form':form}
        return render(request, 'accounts/write_message.html', context)
    
    def post(self, request):
        form = MessageForm(request.POST)
        if request.POST['receiver'] == request.user.username:
            form.add_error('receiver', 'You cannot send a message to yourself.')
        if form.is_valid():
            subject = request.POST['subject']
            body = request.POST['message']
            receiver = request.POST['receiver']
            sender = request.user
            r = User.objects.get(username=receiver)
            m = Message.objects.create(subject=subject,
                                       body=body,
                                       sender=sender,
                                       receiver=r)
            m.save()
            return redirect('accounts:messages')
        else:
            return render(request, 'accounts/write_message.html', {'form':form})
        

class reply_message_view(LoginForm, generic.CreateView):
    def get(self, request, slug):
        message = get_object_or_404(Message, slug_subject=slug)
        form = MessageForm(initial={'receiver':message.sender.username,
                                    'subject':'Re: ' + message.subject,
                                    'message':'''\n----------------------------------------\nPrevious message: \n''' + message.body})
        context = {'form':form}
        return render(request, 'accounts/write_message.html', context)
    
    def post(self, request):
        form = MessageForm(request.POST)
        if request.POST['receiver'] == request.user.username:
            form.add_error('receiver', 'You cannot send a message to yourself.')
        if form.is_valid():
            subject = request.POST['subject']
            body = request.POST['message']
            receiver = request.POST['receiver']
            sender = request.user
            r = User.objects.get(username=receiver)
            m = Message.objects.create(subject=subject,
                                       body=body,
                                       sender=sender,
                                       receiver=r)
            m.save()
            return redirect('accounts:messages')
        else:
            return render(request, 'accounts/write_message.html', {'form':form})