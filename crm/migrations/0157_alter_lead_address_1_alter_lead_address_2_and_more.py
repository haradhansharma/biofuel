# Generated by Django 4.0.1 on 2022-09-06 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0156_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='address_1',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='address_2',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='city',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='455091239889', max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
