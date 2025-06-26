from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from optimal_fuel_path.addresses.services.open_routes_service import (
    OpenRoutesService
)

from . import serializers
from optimal_fuel_path.gas.models import Truckstop


class CheapestFuelRoute(APIView):
    service = OpenRoutesService.create()

    def validate_post_data(self, data):
        serializers.CheapestFuelRouteRequestSerializer(
            data=data
        ).is_valid(raise_exception=True)

    def post(self, request, *args, **kwargs):
        self.validate_post_data(request.data)
        data = self.service.get_route_data(request.data)
        if data is None:
            return Response(
                data={"error": (
                        "There was an error with the map API"
                        " try again later"
                        )
                },
                status=status.HTTP_412_PRECONDITION_FAILED
                )
        cheapest_to_fuel_up = Truckstop.objects.cheapest_to_fuel_up_on_highways(
            data
        )
        return Response(
            data=cheapest_to_fuel_up, 
            status=status.HTTP_200_OK
        )
