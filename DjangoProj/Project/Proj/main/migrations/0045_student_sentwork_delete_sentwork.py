# Generated by Django 4.1.7 on 2023-04-24 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_sentwork'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='sentwork',
            field=models.FileField(null=True, upload_to='works/'),
        ),
        migrations.DeleteModel(
            name='SentWork',
        ),
    ]
