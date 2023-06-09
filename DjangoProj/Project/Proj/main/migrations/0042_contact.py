# Generated by Django 4.1.7 on 2023-04-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_remove_chapter_video_chapter_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('detail', models.TextField(null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '15. Contacts',
            },
        ),
    ]
