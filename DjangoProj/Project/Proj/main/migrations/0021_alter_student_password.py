# Generated by Django 4.1.7 on 2023-04-04 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_student_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
