# Generated by Django 4.1.7 on 2023-03-10 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_course_id_alter_coursecategory_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='featured_img',
            field=models.ImageField(null=True, upload_to='course_imgs/'),
        ),
        migrations.AddField(
            model_name='course',
            name='technologies',
            field=models.TextField(null=True),
        ),
    ]
