# Generated by Django 4.0.1 on 2023-02-17 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0093_suggestions_comitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestions',
            name='su_type',
            field=models.CharField(choices=[('question', 'Question'), ('option', 'Option')], default='question', max_length=10),
        ),
    ]
