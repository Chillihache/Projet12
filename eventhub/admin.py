from django.contrib import admin
from eventhub.models import Client, Contract, Event, CustomUser
from django.contrib.auth.admin import UserAdmin
from eventhub.forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email', 'employee_number', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_active']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'employee_number')}),
        ('Permissions', {'fields': ('groups', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'employee_number', 'first_name', 'last_name',
                       'is_active', 'is_staff'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
