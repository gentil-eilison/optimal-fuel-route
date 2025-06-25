import pathlib
import re

import pandas as pd
from celery import shared_task


from .models import State, City, Address


@shared_task
def import_country_states(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df = df[['State']].drop_duplicates(inplace=False)

    for _, row in df.itertuples():
        State.objects.get_or_create(
            abbreviation=row.upper(),
            defaults={"abbreviation": row.upper()}
        )
    

@shared_task
def import_cities(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df["City"] = df["City"].astype(str).str.strip()
    df["State"] = df["State"].astype(str).str.strip().str.upper()
    df = df[['City', 'State']].drop_duplicates(subset=["City", "State"])

    state_lookup = {state.abbreviation: state for state in State.objects.all()}

    for _, city, state in df.itertuples():
        City.objects.get_or_create(
            name=city,
            country_state=state_lookup[state],
            defaults={
                "name": city,
                "country_state": state_lookup[state]
            }
        )


@shared_task
def import_addresses(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df["Address"] = df["Address"].astype(str).str.upper().str.strip()
    df["City"] = df["City"].astype(str).str.strip()
    df["State"] = df["State"].astype(str).str.upper().str.strip()
    df = df[["Address", "City", "State"]]

    highways_pattern = re.compile(r"(?:[A-Z]+-[0-9]+)|(?:EXIT\s[0-9]+)")
    cities_lookup = {
        f"{city.name}-{city.country_state.abbreviation}": city
        for city in City.objects.all()
    }

    for _, address, city, state in df.itertuples():
        city_obj = cities_lookup[f"{city}-{state}"]
        highways = highways_pattern.findall(address)
        for highway in highways:
            address, _ = Address.objects.get_or_create(address=address)
            address.cities.add(city_obj)
