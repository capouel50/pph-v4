# Generated by Django 4.2.3 on 2024-01-27 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0065_categoriematiere'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typematiere',
            name='logo',
        ),
    ]
