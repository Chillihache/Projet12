from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Client

@receiver(pre_save, sender=Client)
def validate_sales_contact_group(sender, instance, **kwargs):
    # Check if a sales_contact is assigned
    if instance.sales_contact:
        # Verify if the user belongs to the 'COMMERCIAL' group
        if not instance.sales_contact.groups.filter(name='Commercial').exists():
            raise ValidationError(f"The user {instance.sales_contact} must belong to the COMMERCIAL group.")