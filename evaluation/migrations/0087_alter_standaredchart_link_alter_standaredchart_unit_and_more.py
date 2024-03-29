# Generated by Django 4.0.1 on 2022-11-09 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_quotation_show_alternate_phone'),
        ('evaluation', '0086_alter_stdoils_biofuel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standaredchart',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='standaredchart',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chrartunit', to='home.weightunit'),
        ),
        migrations.AlterField(
            model_name='standaredchart',
            name='value',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
    ]
