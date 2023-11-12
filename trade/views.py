from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from plant_collection.models import Plant
from .models import Trade
from django.http import Http404, HttpResponse

"""
This view is for making trade between two plants.
It is receiving two kinds of get requests: one for ajax request for user requesting trade and one for displaying desired plant.
"""
class trade(LoginRequiredMixin, View):
    def get(self, request, req):
        # This is for ajax request to return plant that user selected as to be traded
        try:
            plant = get_object_or_404(Plant, nick_name=request.GET["plant"].strip())
            return render(
                request, "trades/assets/trade_offered_plant.html", {"plant": plant}
            )
        except:
            pass
        req_plant = get_object_or_404(Plant, slug=req)
        return render(request, "trades/trade.html", {"req": req_plant})

    # Two plants are posted and trade is made between their owners
    def post(self, request, req):
        offered = get_object_or_404(Plant, nick_name=request.POST["offered"])
        requested = get_object_or_404(Plant, nick_name=request.POST["requested"])
        initiator = request.user
        recipient = requested.owner
        errors = []
        # Checking wheter user is not trying to trade with himself, wheter he has not already made this trade
        if offered.owner == recipient:
            errors.append("You cannot trade with yourself.")
        if Trade.objects.filter(
            plant_offered=offered,
            plant_requested=requested,
            initiator=initiator,
            recipient=recipient,
        ):
            errors.append("You have already made this trade.")
        elif Trade.objects.filter(
            plant_offered=requested,
            plant_requested=offered,
            initiator=recipient,
            recipient=initiator,
        ):
            errors.append("This trade already exists.")
        if errors:
            return render(
                request,
                "trades/trade.html",
                {"req": requested, "errors": errors},
            )
        trade = Trade.objects.create(
            plant_offered=offered,
            plant_requested=requested,
            initiator=initiator,
            recipient=recipient,
        )
        trade.save()
        return redirect("plant_collection:personal_collection")


"""
This view is for displaying all trades that given plant is involved in.
"""
class plant_offers(LoginRequiredMixin, generic.View):
    template_name = "trades/plant_offers.html"
    def get(self, request, slug):
        plant = get_object_or_404(Plant, slug=slug)
        if request.user == plant.owner:
            # Showing only trades that are not finalized
            req = Trade.objects.filter(plant_requested=plant, finalized=False)
            offered = Trade.objects.filter(plant_offered=plant, finalized=False)
            context = {"offers": offered, "requests": req, "plant": plant}
            return render(request, self.template_name, context)
        return redirect("plant_collection:front_page")
    

class trades_view(LoginRequiredMixin, generic.View):
    template_name = 'trades/offers.html'
    def get(self, request):
        #Show all trades that are not finalized
        req = Trade.objects.filter(recipient=request.user, finalized=False)
        offered = Trade.objects.filter(initiator=request.user, finalized=False)
        print(req, offered)
        context = {'offers':offered, 'requests':req}
        return render(request, self.template_name, context)
    

'''
This view is for showing the trade details and finalizing the trade.
It receives 2 kinds of POST requests: One for accepting/declining/retracting a trade, and the other for finalizing a trade.
'''
class trade_final(LoginRequiredMixin, generic.View):
    template_name = 'trades/trade_final.html'
    def get(self, request, pk):
        trade = get_object_or_404(Trade, pk=pk)
        context = {'trade':trade}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        #This part is for accepting or declining a trade
        decline = request.POST.get('decline', None)
        accept = request.POST.get('accept', None)
        retract = request.POST.get('retract', None)
        if decline:
            trade = get_object_or_404(Trade, pk=pk)
            trade.decline()
            req = Trade.objects.filter(recipient=request.user, finalized=False)
            offered = Trade.objects.filter(initiator=request.user, finalized=False)
            confirm = 'Trade offer was declined.'
            context = {'offers':offered, 'requests':req, 'confirmations': confirm}
            return render(request, 'trades/offers.html', context)
        if accept:
            trade = get_object_or_404(Trade, pk=pk)
            trade.accept()
            req = Trade.objects.filter(recipient=request.user, finalized=False)
            offered = Trade.objects.filter(initiator=request.user, finalized=False)
            confirm = 'Trade offer was accepted.'
            context = {'offers':offered, 'requests':req, 'confirmations': confirm}
            return render(request, 'trades/offers.html', context)
        if retract:
            trade = get_object_or_404(Trade, pk=pk)
            trade.decline()
            req = Trade.objects.filter(recipient=request.user, finalized=False)
            offered = Trade.objects.filter(initiator=request.user, finalized=False)
            confirm = 'Trade offer was retracted.'
            context = {'offers':offered, 'requests':req, 'confirmations': confirm}
            return render(request, 'trades/offers.html', context)


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
        if finalize and request.user.username == str(trade.recipient):
            trade.requested_finalized = True
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 green-check sendable")
        if not finalize and request.user.username == str(trade.initiator):
            trade.offered_finalized = False
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 red-check sendable")
        if not finalize and request.user.username == str(trade.recipient):
            trade.requested_finalized = False
            trade.save()
            return HttpResponse("fa-solid fa-circle-check is-size-1 red-check sendable")
        raise Http404("You are not authorized to do that.")