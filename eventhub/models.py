from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        if not extra_fields.get('employee_number'):
            raise ValueError("Le numéro d'employé est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    employee_number = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_number', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    email = models.EmailField(verbose_name="email")
    company_name = models.CharField(max_length=50, verbose_name="Company name")

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Last update date")

    sales_contact = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Sales contact")

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

    support_contact = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Support contact")
    location = models.CharField(max_length=100, verbose_name="Location")
    attendees = models.PositiveIntegerField(verbose_name="Number of attendees")
    notes = models.TextField(verbose_name="Notes")

    class Meta:
        permissions = [("change_event_support_contact",
                        "Peut associer un collaborateur de l'équipe support à l'évennement"),
                       ("filter_events", "Peut filtrer les évennements")]

    def __str__(self):
        return f"{name}"


