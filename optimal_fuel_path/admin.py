from django.contrib import admin, messages
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from optimal_fuel_path.gas.forms import ImportTruckstopDataForm
from optimal_fuel_path.addresses.tasks import (
    import_country_states, 
    import_cities,
    import_addresses
)
from optimal_fuel_path.gas.tasks import import_truckstops


class GasAdminSite(admin.AdminSite):
    site_title = "Economic Car Trip"

    def get_urls(self):
        additional_urls = [
            path("truckstop-import/", self.truckstop_import_view),
        ]
        urls = super().get_urls()
        return additional_urls + urls
    
    def truckstop_import_view(self, request):
        context = dict(
            self.each_context(request)
        )
        form = None
        if request.method == "GET":
            form = ImportTruckstopDataForm()
        else:
            form = ImportTruckstopDataForm(request.POST)
            form.files = request.FILES
            if form.is_valid():
                messages.add_message(
                    request, 
                    level=messages.SUCCESS, 
                    message="Import started. It might take a while..."
                )
                temp_file = request.FILES["csv_file"]
                fs = FileSystemStorage(location="/home/cvstodia/Documents")
                filename = fs.save(temp_file.name, temp_file)
                full_path = fs.path(filename)
                import_truckstops.delay(full_path)
                return HttpResponseRedirect("/admin/")
        
        context.update({"import_form": form})
        return TemplateResponse(request, "gas/truckstop_import.html", context)
