# Generated by Django 4.0.1 on 2023-02-10 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_rename_type_user_usertype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined']},
        ),
        migrations.AddField(
            model_name='profile',
            name='company_logo',
            field=models.ImageField(default='', upload_to='company_logo'),
            preserve_default=False,
        ),
    ]
