from django.contrib import admin
from eventhub.models import Client, Contract, Event, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'email', 'employee_number', 'is_staff', 'is_active')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'employee_number'),
        }),
    )



admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
admin.site.register(User, UserAdmin)