from typing import Any

from django.db.models import QuerySet


class TruckstopQuerySet(QuerySet):
    def on_highways(self, highways: list[str]):
        return self.filter(addresses__address__in=highways)

    def cheapest_to_fuel_up_on_highways(
        self, 
        route_data: dict[str, Any]
    ) -> dict[str, Any]:
        highways, fuel_up_count = route_data.get("highways"), route_data.get("fuel_up_count")
        data = {
            "truckstops": [], 
            "total_cost": 0, 
            "map_data": route_data["map_data"]
        }
        truckstops = list(self.on_highways(highways).values_list(
            "opis",
            "name",
            "retail_price"
        ))
        for _ in range(fuel_up_count):
            # Data at index 2 will be the retail_price
            # Use that to get the cheapest
            cheapest_truckstop = min(truckstops, key=lambda data: data[2])
            opis, name, retail_price = cheapest_truckstop
            data["truckstops"].append({
                "opis": opis,
                "name": name,
                "retail_price": retail_price
            })
            # The vehicle can run 10 miles with a galon.
            # It can run a total of 500 miles until it runs out of
            # gas. So it must get 50 (500/10) gallons at each
            # gas station
            data["total_cost"] = data["total_cost"] + 50 * retail_price
            # Remove it so that it's not selected again
            truckstops.remove(cheapest_truckstop)
        
        data["total_cost"] = round(data["total_cost"], 2)
        
        return data
