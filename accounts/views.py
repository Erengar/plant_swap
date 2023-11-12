from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout,authenticate
from .forms import LoginForm, RegistrationForm, MessageForm
from django.contrib.auth.models import User
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from plant_collection.models import Plant
from django.http import Http404
from .models import Message
from django.core.management import call_command

class login_view(LoginView):
    template_name = 'accounts/login.html'
    next_page = ('plant_collection:personal_collection')
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def post(self, request):
        form = LoginForm(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('plant_collection:front_page')
        return render(request, self.template_name, {'form':form, 'error': 'Invalid username or password.'})

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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            c = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'])
            c.save()
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('plant_collection:front_page')
        return render(request, self.template_name, {'form':form})
          

'''
This view is for showing plants user have liked.
'''
class liked_list(LoginRequiredMixin, generic.View):
    template_name = 'accounts/like_list.html'
    def get(self, request, order='-likes'):
        context = {'plants':Plant.objects.filter(likes=request.user).order_by(order)}
        return render(request, self.template_name, context)
    

'''
This receives receives GET and POST requests. It show all sent and received messages and allows delete of messages.
'''
class messages_view(LoginRequiredMixin, generic.View):
    def get(self, request, order='-date_sent'):
        context = {}
        messages = Message.objects.filter(receiver=request.user).order_by(order, '-date_sent')
        #If the url contains 'sent', it shows sent messages instead of received messages
        if 'sent' in request.build_absolute_uri():
            messages = Message.objects.filter(sender=request.user).order_by(order, '-date_sent')
            context['sent'] = True
        context['messages'] = messages
        context['order'] = order
        return render(request, 'accounts/messages.html', context)
    
    def post(self, request):
        for req in request.POST:
            if req != 'csrfmiddlewaretoken':
                m = Message.objects.get(slug_subject=req)
                if request.user == m.sender:
                    m.sender = None
                    m.save()
                else:
                    m.receiver = None
                    m.save()
        return redirect('accounts:messages')


'''
This receives only GET request, but need additional parameter for identifying message to display.
It is for showing the message. It also marks the message as read.
'''
class message_view(LoginRequiredMixin, generic.View):
    def get(self, request, slug):
        message = get_object_or_404(Message, slug_subject=slug)
        if request.user not in (message.receiver, message.sender):
            raise Http404("You are not authorized to do that.")
        message.read = True
        message.save()
        context = {'message':message}
        return render(request, 'accounts/message.html', context)



'''
This view receives both GET and POST requests. It is for writing a message. It is utilizing django forms.
'''
class write_message_view(LoginRequiredMixin, generic.View):
    def get(self, request, name):
        if name== '@':
            form = MessageForm
        else:
            form = MessageForm(initial={'receiver':name})
        context = {'form':form}
        return render(request, 'accounts/write_message.html', context)
    
    def post(self, request, name):
        form = MessageForm(request.POST)
        if request.POST['receiver'] == request.user.username:
            form.add_error('receiver', 'You cannot send a message to yourself.')
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']
            receiver = form.cleaned_data['receiver']
            sender = request.user
            r = User.objects.get(username=receiver)
            m = Message.objects.create(subject=subject,
                                       body=body,
                                       sender=sender,
                                       receiver=r)
            m.save()
            return redirect('accounts:messages')
        return render(request, 'accounts/write_message.html', {'form':form})
        

'''
This is variation of write_message_view. It is for replying to a message. It receives only GET and POST request.
'''
class reply_message_view(LoginForm, generic.View):
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
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']
            receiver = form.cleaned_data['receiver']
            sender = request.user
            r = User.objects.get(username=receiver)
            m = Message.objects.create(subject=subject,
                                       body=body,
                                       sender=sender,
                                       receiver=r)
            m.save()
            return redirect('accounts:messages')
        return render(request, 'accounts/write_message.html', {'form':form})
    
class profile_view(LoginRequiredMixin, generic.View):
    def get(self, request):
        context = {'user':request.user}
        return render(request, 'accounts/profile.html', context)

def seed_plants(request):
    call_command('populate_plants')
    return redirect('plant_collection:front_page')

def clean_plants(request):
    call_command('depopulate_plants')
    return redirect('plant_collection:front_page')

def delete_profile(request):
    request.user.delete()
    return redirect('plant_collection:front_page')