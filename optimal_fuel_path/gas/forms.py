from django import forms


class ImportTruckstopDataForm(forms.Form):
    csv_file = forms.FileField(label="Truckstop CSV", required=True)
