# Generated by Django 4.1.7 on 2023-04-18 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('answer', models.TextField(null=True)),
            ],
            options={
                'verbose_name_plural': '16. FAQ',
            },
        ),
    ]
