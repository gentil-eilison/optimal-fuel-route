from rest_framework import serializers
from ..models import Truckstop

class CheapestFuelRouteRequestSerializer(serializers.Serializer):
    departure = serializers.ListField(
        required=True,
        child=serializers.FloatField()
    )
    destination = serializers.ListField(
        required=True,
        child=serializers.FloatField()
    )


class TruckstopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truckstop
        fields = ("opis", "name", "retail_price")
