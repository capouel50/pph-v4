# Generated by Django 4.2.3 on 2023-12-31 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0030_catalogue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
    ]
