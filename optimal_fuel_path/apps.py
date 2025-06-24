from django.contrib.admin.apps import AdminConfig


class GasAdminConfig(AdminConfig):
    default_site = "optimal_fuel_path.admin.GasAdminSite"