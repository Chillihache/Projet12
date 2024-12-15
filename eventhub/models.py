from django.db import models
from django.core.validators import MinValueValidator
import uuid

from authentication.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    email = models.EmailField(verbose_name="email")
    company_name = models.CharField(max_length=50, verbose_name="Company name")

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Last update date")

    sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Sales contact")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="UUID")

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name="Client")

    total_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                       validators=[MinValueValidator(0)], verbose_name="Total amount")
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                           validators=[MinValueValidator(0)],
                                           verbose_name="Remaining amount")

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    is_signed = models.BooleanField(default=False, verbose_name="Is signed")


class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name="Contract")

    event_date_start = models.DateTimeField(verbose_name="Event date start")
    event_date_end = models.DateTimeField(verbose_name="Event date end")

    support_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Support contact")
    location = models.CharField(max_length=100, verbose_name="Location")
    attendees = models.PositiveIntegerField(verbose_name="Number of attendees")
    notes = models.TextField(verbose_name="Notes")

    def __str__(self):
        return f"{name}"


