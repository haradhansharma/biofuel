# Generated by Django 4.0.1 on 2022-04-18 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_alter_quotation_related_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='quotationserviceprovider', to=settings.AUTH_USER_MODEL),
        ),
    ]
