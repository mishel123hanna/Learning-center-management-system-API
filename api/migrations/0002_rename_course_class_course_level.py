# Generated by Django 4.1.7 on 2023-04-10 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_class',
            new_name='level',
        ),
    ]