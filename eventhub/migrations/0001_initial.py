# Generated by Django 5.1.4 on 2024-12-14 19:41

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('company_name', models.CharField(max_length=50, verbose_name='Company name')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Last update date')),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Sales contact')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='UUID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total amount')),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Remaining amount')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('is_signed', models.BooleanField(default=False, verbose_name='Is signed')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eventhub.client', verbose_name='Client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('event_date_start', models.DateTimeField(verbose_name='Event date start')),
                ('event_date_end', models.DateTimeField(verbose_name='Event date end')),
                ('location', models.CharField(max_length=100, verbose_name='Location')),
                ('attendees', models.PositiveIntegerField(verbose_name='Number of attendees')),
                ('notes', models.TextField(verbose_name='Notes')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventhub.contract', verbose_name='Contract')),
                ('support_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Support contact')),
            ],
        ),
    ]
