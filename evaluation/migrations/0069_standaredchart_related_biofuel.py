# Generated by Django 4.0.1 on 2022-11-01 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0068_reportmailqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='standaredchart',
            name='related_biofuel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_biofuel', to='evaluation.biofuel'),
        ),
    ]
