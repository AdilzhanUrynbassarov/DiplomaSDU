# Generated by Django 4.1.7 on 2023-03-19 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_user_delete_student'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Student',
        ),
    ]
