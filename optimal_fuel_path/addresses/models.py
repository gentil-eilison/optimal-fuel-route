from django.db import models
from django.utils.translation import gettext_lazy as _

from optimal_fuel_path.core import models as core_models


class State(core_models.TimeStampedModel):
    abbreviation = models.CharField(
        max_length=2, 
        verbose_name=_("Abbreviation"),
        unique=True
    )

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
    
    def __str__(self):
        return self.abbreviation


class City(core_models.TimeStampedModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )
    country_state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        related_name="cities",
        verbose_name=_("Country State")
    )

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country_state"],
                name="unique_city_name_country_state"
            )
        ]
    
    def __str__(self):
        return f"{self.name} - {self.country_state.abbreviation}"


class Address(core_models.TimeStampedModel):
    city = models.ManyToManyField(
        City,
        related_name="addresses",
        verbose_name=_("City")
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_("Address")
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.address
