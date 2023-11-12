from django.db import models
from django.conf import settings
from plant_collection.models import Plant



class Trade(models.Model):
    plant_offered = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="trades_offered"
    )
    plant_requested = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="trades_requested"
    )
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trades_initiated",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trades_received",
    )
    accepted = models.BooleanField(null=True, blank=True)
    offered_finalized = models.BooleanField(default=False)
    requested_finalized = models.BooleanField(default=False)
    finalized = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ["plant_offered", "plant_requested"]

    def accept(self):
        self.accepted = True
        self.save()

    def decline(self):
        self.accepted = False
        self.delete()

    def exchange(self):
        self.plant_offered.owner = self.recipient
        self.plant_requested.owner = self.initiator
        self.plant_offered.save()
        self.plant_requested.save()

    def __str__(self):
        return f"{self.plant_offered} for {self.plant_requested}"