# Generated by Django 4.1.7 on 2023-03-12 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_course_featured_img_course_technologies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='featured_img',
            field=models.ImageField(null=True, upload_to='featured_imgs/'),
        ),
    ]
