# Generated by Django 4.1.5 on 2023-01-06 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0009_alter_appointment_zoom_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='teacher',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
