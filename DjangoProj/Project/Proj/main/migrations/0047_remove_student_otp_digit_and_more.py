# Generated by Django 4.1.7 on 2023-04-26 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_remove_student_sentwork'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='otp_digit',
        ),
        migrations.RemoveField(
            model_name='student',
            name='verify_status',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='otp_digit',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='verify_status',
        ),
    ]