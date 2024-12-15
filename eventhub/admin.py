from django.contrib import admin
from eventhub.models import Client, Contract, Event


admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
