from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from sentry_sdk import capture_message
from eventhub.models import Client, Event, CustomUser, Contract


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


@receiver(post_save, sender=CustomUser)
def sentry_alert_user_saved(sender, instance, created, **kwargs):
    action = "créé" if created else "modifié"
    capture_message(f"Le collaborateur {instance.first_name} {instance.last_name} a été {action}")


@receiver(pre_save, sender=Contract)
def sentry_alert_contract_signed(sender, instance, **kwargs):
    try:
        contract = Contract.objects.get(id=instance.id)
        if not contract.is_signed and instance.is_signed:
            capture_message(f"Le contrat {instance.contract_number} a été signé.")
    except Contract.DoesNotExist:
        if instance.is_signed:
            capture_message(f"Le contrat {instance.contract_number} a été signé.")
