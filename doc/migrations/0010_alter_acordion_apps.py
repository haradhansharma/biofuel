# Generated by Django 4.0.1 on 2022-05-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0009_alter_acordion_apps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acordion',
            name='apps',
            field=models.CharField(choices=[('administration', 'Administration'), ('authentication-and-authorization', 'Authentication and Authorization'), ('content-types', 'Content Types'), ('sessions', 'Sessions'), ('messages', 'Messages'), ('static-files', 'Static Files'), ('debug-toolbar', 'Debug Toolbar'), ('sites', 'Sites'), ('axes', 'Axes'), ('accounts', 'Accounts'), ('home', 'Home'), ('evaluation', 'Evaluation'), ('crm', 'Crm'), ('doc', 'Doc'), ('django-recaptcha', 'Django reCAPTCHA'), ('guide', 'Guide')], max_length=50),
        ),
    ]
