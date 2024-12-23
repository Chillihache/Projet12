from django.contrib import admin
from eventhub.models import Client, Contract, Event, User


admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
admin.site.register(User)