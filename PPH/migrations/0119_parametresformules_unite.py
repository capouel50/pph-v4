# Generated by Django 4.2.3 on 2024-02-23 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0118_articlesformules'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametresformules',
            name='unite',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
