# Generated by Django 4.0.1 on 2022-09-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0162_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='931839369829', max_length=50),
        ),
    ]
