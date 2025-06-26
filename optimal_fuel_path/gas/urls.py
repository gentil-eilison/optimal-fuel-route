from django.urls import path

from .api import views


app_name = "gas"

urlpatterns = [
    path(
        "truckstop-cheapest/", 
        views.CheapestFuelRoute.as_view(), 
        name="truckstop_cheapest"
    )
]