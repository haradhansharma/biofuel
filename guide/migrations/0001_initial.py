# Generated by Django 4.0.1 on 2022-06-01 09:39

from django.db import migrations, models
# import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenarelGUide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=252)),
                ('anchor', models.CharField(max_length=252)),
                # ('content', tinymce.models.HTMLField()),
            ],
        ),
    ]
