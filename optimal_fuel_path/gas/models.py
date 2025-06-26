from django.db import models
from django.utils.translation import gettext_lazy as _

from optimal_fuel_path.core import models as core_models
from optimal_fuel_path.addresses import models as addresses_models

from .querysets import TruckstopQuerySet

class Truckstop(core_models.TimeStampedModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    opis = models.PositiveIntegerField(
        verbose_name=_("OPIS"),
    )
    rack_id = models.PositiveIntegerField(
        verbose_name=_("Rack ID")
    )
    retail_price = models.FloatField(
        verbose_name=_("Retail Price")
    )
    addresses = models.ManyToManyField(
        addresses_models.Address,
        related_name="truckstops",
        verbose_name=_("Addresses")
    )

    objects: TruckstopQuerySet = TruckstopQuerySet.as_manager()

    class Meta:
        verbose_name = _("Truckstop")
        verbose_name_plural = _("Truckstops")
    
    def __str__(self):
        return f"{self.opis} - {self.name}"
