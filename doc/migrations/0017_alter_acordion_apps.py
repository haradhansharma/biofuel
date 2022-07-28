# Generated by Django 4.0.1 on 2022-07-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0016_exsite_site_meta_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acordion',
            name='apps',
            field=models.CharField(choices=[('administration', 'Administration'), ('authentication-and-authorization', 'Authentication and Authorization'), ('content-types', 'Content Types'), ('sessions', 'Sessions'), ('messages', 'Messages'), ('static-files', 'Static Files'), ('ckeditor', 'Ckeditor'), ('ckeditor_uploader', 'Ckeditor_Uploader'), ('debug-toolbar', 'Debug Toolbar'), ('sites', 'Sites'), ('axes', 'Axes'), ('accounts', 'Accounts'), ('home', 'Home'), ('evaluation', 'Evaluation'), ('crm', 'Crm'), ('doc', 'Doc'), ('django-recaptcha', 'Django reCAPTCHA'), ('guide', 'Guide'), ('maintenance_mode', 'Maintenance_Mode')], max_length=50),
        ),
    ]
