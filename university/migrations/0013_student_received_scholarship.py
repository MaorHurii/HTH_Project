# Generated by Django 4.1.5 on 2023-01-06 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0012_answer_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='received_scholarship',
            field=models.BooleanField(default=False),
        ),
    ]
