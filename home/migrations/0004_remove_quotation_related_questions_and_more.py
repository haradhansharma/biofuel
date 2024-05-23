# Generated by Django 4.0.1 on 2022-04-16 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0036_question_chapter_name'),
        ('home', '0003_quotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='related_questions',
        ),
        migrations.AddField(
            model_name='quotation',
            name='related_questions',
            field=models.ManyToManyField(help_text='Help Text will go here', to='evaluation.Question', verbose_name='Please select all other question which are also tested within the provided quotation'),
        ),
    ]
