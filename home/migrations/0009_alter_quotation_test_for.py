# Generated by Django 4.0.1 on 2022-04-18 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0036_question_chapter_name'),
        ('home', '0008_alter_quotation_service_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='test_for',
            field=models.ForeignKey(help_text='Help Text will go here', max_length=252, on_delete=django.db.models.deletion.CASCADE, related_name='testfor', to='evaluation.question', verbose_name='Tests for question'),
        ),
    ]
