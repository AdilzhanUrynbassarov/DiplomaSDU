# Generated by Django 4.1.7 on 2023-04-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_userassignment_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassignment',
            name='user_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
