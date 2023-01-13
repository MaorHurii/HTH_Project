# Generated by Django 4.1.5 on 2023-01-05 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0007_delete_report_rename_answer_answer_body_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='question',
            name='creator',
            field=models.CharField(default='student', max_length=255),
            preserve_default=False,
        ),
    ]
