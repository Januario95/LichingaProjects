# Generated by Django 4.2.1 on 2023-05-25 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_quantity_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='budget',
        ),
    ]
