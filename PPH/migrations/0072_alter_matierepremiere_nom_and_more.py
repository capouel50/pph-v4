# Generated by Django 4.2.3 on 2024-01-29 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0071_matierepremiere_unite_mesure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matierepremiere',
            name='nom',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='matierepremiere',
            name='prix_unit',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
