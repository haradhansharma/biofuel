# Generated by Django 4.0.1 on 2022-11-03 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0201_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='921646802176', max_length=50),
        ),
    ]
