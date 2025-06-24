import pathlib

import pandas as pd
from celery import shared_task


from .models import State, City

def import_country_states(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df = df[['State']].drop_duplicates(inplace=False)

    for _, row in df.itertuples():
        State.objects.get_or_create(
            abbreviation=row.upper(),
            defaults={"abbreviation": row.upper()}
        )
    

def import_cities(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df["City"] = df["City"].astype(str).str.strip().str.title()
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


def import_addresses(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df["Addresses"] = df["Addresses"].astype(str).str.upper()
    df = df[["Addresses"]].drop_duplicates(subset=["Addresses"])

    regex = r"(?:[A-Z]+-[0-9]+)|(?:EXIT\s[0-9]+)"
