import pathlib
import pandas as pd
import re

from celery import shared_task

from .models import Truckstop
from optimal_fuel_path.addresses.models import Address


@shared_task
def import_truckstops(csv_path: str):
    df = pd.read_csv(pathlib.Path(csv_path))
    df["Address"] = df["Address"].astype(str).str.upper().str.strip()
    df["City"] = df["City"].astype(str).str.strip()
    df["State"] = df["State"].astype(str).str.strip()
    df["Truckstop Name"] = df["Truckstop Name"].astype(str).str.strip()
    df["Retail Price"] = df["Retail Price"].astype(float)
    df["Rack ID"] = df["Rack ID"].astype(float)
    df["OPIS Truckstop ID"] = df["OPIS Truckstop ID"].astype(float)
    df = df.drop_duplicates()

    existing_truckstops = tuple(
        Truckstop.objects.values_list("opis", "name", "rack_id", "retail_price")
    )
    truckstops = []

    for _, opis, truckstop, address, _, _, rack_id, retail_price in df.itertuples():
        if (opis, truckstop, rack_id, retail_price) not in existing_truckstops:
            truckstops.append(Truckstop(
                opis=opis,
                name=truckstop,
                rack_id=rack_id,
                retail_price=retail_price,
            ))
    
    Truckstop.objects.bulk_create(
        truckstops, 
        ignore_conflicts=True
    )

    highways_pattern = re.compile(r"(?:[A-Z]+-[0-9]+)|(?:EXIT\s[0-9]+)")
    for _, opis, truckstop, address, _, _, rack_id, retail_price in df.itertuples():
        truckstop_obj = Truckstop.objects.filter(
            opis=opis,
            rack_id=rack_id,
            retail_price=retail_price,
        ).first()
        highways = highways_pattern.findall(address)
        highways_objs = Address.objects.filter(address__in=highways)
        truckstop_obj.addresses.set(highways_objs)
