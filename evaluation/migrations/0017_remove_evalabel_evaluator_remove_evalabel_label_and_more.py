# Generated by Django 4.0.1 on 2022-03-30 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0016_alter_evaluator_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evalabel',
            name='evaluator',
        ),
        migrations.RemoveField(
            model_name='evalabel',
            name='label',
        ),
        migrations.RemoveField(
            model_name='evalebelstatement',
            name='evalebel',
        ),
        migrations.RemoveField(
            model_name='evalebelstatement',
            name='evaluator',
        ),
        migrations.RemoveField(
            model_name='evalebelstatement',
            name='question',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='evaluator',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='option',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='question',
        ),
        migrations.RemoveField(
            model_name='evaluator',
            name='biofuel',
        ),
        migrations.RemoveField(
            model_name='evaluator',
            name='creator',
        ),
        migrations.DeleteModel(
            name='EvaComments',
        ),
        migrations.DeleteModel(
            name='EvaLabel',
        ),
        migrations.DeleteModel(
            name='EvaLebelStatement',
        ),
        migrations.DeleteModel(
            name='Evaluation',
        ),
        migrations.DeleteModel(
            name='Evaluator',
        ),
    ]
