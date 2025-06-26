from typing import Any

import requests
import os
import json
import re


class OpenRoutesService:
    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url
    
    @staticmethod
    def create():
        return OpenRoutesService(
            os.environ.get("OPENROUTES_API_KEY"),
            "https://api.openrouteservice.org/v2"
        )

    def get_directions_for(
        self, 
        departure: list[float, float], 
        destination: list[float, float]
    ) -> requests.Response:
        return requests.post(
            f"{self._base_url}/directions/driving-hgv",
            headers={
                "Authorization": self._api_key,
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "coordinates": [departure, destination],
                "instructions": True,
                "extra_info": ["waytype"],
                "units": "mi"
            })
        )

    def get_route_data(
        self,
        trip: dict[str, list[int]]
    ) -> dict[str, Any] | None:
        response = self.get_directions_for(
            trip.get("departure"), 
            trip.get("destination")
        )
        if not response.ok:
            return None

        highways = set()
        data = response.json()

        if data.get("routes"):
            segments = data.get("routes")[0].get("segments")
            for segment in segments:
                for step in segment.get("steps"):
                    if step.get("name"):
                        found_highways = re.findall(r"[A-Z]+[\s-][0-9]+", step.get("name"))
                        if found_highways:
                            found_highways = set(map(
                                lambda highway: highway.replace(" ", "-"),
                                found_highways
                            ))
                            highways = highways.union(found_highways)
            response = {
                "highways": highways,
                "fuel_up_count": self.calculate_fuel_up_count(
                    data.get("routes")[0].get("summary").get("distance")
                ),
                "map_data": data
            }
            return response

    def calculate_fuel_up_count(self, total_miles: float) -> int:
        return round(total_miles / 500)
