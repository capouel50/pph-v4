# Generated by Django 4.2.3 on 2024-02-13 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0080_alter_matierepremiere_qté_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reception',
            name='stock_reception',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]