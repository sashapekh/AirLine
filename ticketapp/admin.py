from django.contrib import admin
from .models import *
from django.apps import apps

# Register your models here.

for model in apps.get_app_config('ticketapp').models.values():
    admin.site.register(model)
