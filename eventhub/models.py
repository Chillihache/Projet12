from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("L'email doit être défini")
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        extra_fields.setdefault("username", email)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    employee_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Numéro d'employé"
    )

    username = models.CharField(max_length=255, unique=False, blank=True)

    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "employee_number"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

    class Meta:
        permissions = [("filter_contracts", "Peut filtrer les contrats")]


class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name="Contract")

    event_date_start = models.DateTimeField(verbose_name="Event date start")
    event_date_end = models.DateTimeField(verbose_name="Event date end")

    support_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Support contact")
    location = models.CharField(max_length=100, verbose_name="Location")
    attendees = models.PositiveIntegerField(verbose_name="Number of attendees")
    notes = models.TextField(verbose_name="Notes")

    class Meta:
        permissions = [("change_event_support_contact",
                        "Peut associer un collaborateur de l'équipe support à l'évennement"),
                       ("filter_events", "Peut filtrer les évennements")]

    def __str__(self):
        return f"{name}"


