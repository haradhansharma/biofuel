# Generated by Django 4.0.1 on 2022-05-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0053_alter_question_chart_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='evalebelstatement',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluator',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluatoractivities',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluatoractivities',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='nextactivities',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='nextactivities',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='optionset',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='optionset',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
