# Generated by Django 4.0.1 on 2022-12-01 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0089_alter_stdoils_select_oil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluator',
            name='orgonization',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='evaluator',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
