# Generated by Django 4.0.1 on 2022-10-12 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0189_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='406192295364', max_length=50),
        ),
    ]
