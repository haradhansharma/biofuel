# Generated by Django 4.0.1 on 2022-02-26 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_mailqueue_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='811716546877', max_length=50),
        ),
        migrations.AlterField(
            model_name='mailqueue',
            name='process_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
