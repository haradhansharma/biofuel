# Generated by Django 4.0.1 on 2022-03-25 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertype',
            name='active',
            field=models.CharField(max_length=255),
        ),
    ]
