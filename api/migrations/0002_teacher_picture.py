# Generated by Django 4.1.7 on 2023-08-13 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='picture',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
