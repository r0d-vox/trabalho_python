# Generated by Django 5.1.3 on 2024-11-20 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perguntadiaria',
            name='tags',
        ),
    ]
