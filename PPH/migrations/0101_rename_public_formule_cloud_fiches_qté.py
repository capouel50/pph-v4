# Generated by Django 4.2.3 on 2024-02-19 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0100_remove_fiches_public_formule_controleur_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formule',
            old_name='public',
            new_name='cloud',
        ),
        migrations.AddField(
            model_name='fiches',
            name='qté',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
