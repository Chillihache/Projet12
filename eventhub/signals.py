from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from eventhub.models import Client, Event

@receiver(pre_save, sender=Client)
def validate_sales_contact_group(sender, instance, **kwargs):
    if instance.sales_contact:
        if not instance.sales_contact.groups.filter(name='Sales').exists():
            raise ValidationError(f"The user {instance.sales_contact} must belong to the COMMERCIAL group.")

@receiver(pre_save, sender=Event)
def validate_support_contact_group(sender, instance, **kwargs):
    if instance.support_contact:
        if not instance.support_contact.groups.filter(name='Support').exists():
            raise ValidationError(f"The user {instance.support_contact} must belong to the SUPPORT group")