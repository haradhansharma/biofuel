# Generated by Django 4.0.1 on 2022-02-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_usertype_created_alter_usertype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertype',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
