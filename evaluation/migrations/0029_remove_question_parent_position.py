# Generated by Django 4.0.1 on 2022-04-02 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0028_question_parent_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='parent_position',
        ),
    ]
