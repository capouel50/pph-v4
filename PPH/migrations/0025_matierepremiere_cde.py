# Generated by Django 4.2.3 on 2023-12-14 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0024_rename_qté_mesure_forme_unite_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='matierepremiere',
            name='cde',
            field=models.BooleanField(default=False),
        ),
    ]
