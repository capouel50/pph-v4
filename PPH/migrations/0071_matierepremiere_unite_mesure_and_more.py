# Generated by Django 4.2.3 on 2024-01-29 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0070_remove_catalogue_cdt_remove_catalogue_forme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matierepremiere',
            name='unite_mesure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.unitemesure'),
        ),
        migrations.AlterField(
            model_name='matierepremiere',
            name='cdt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.conditionnement'),
        ),
        migrations.AlterField(
            model_name='matierepremiere',
            name='forme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.forme'),
        ),
        migrations.AlterField(
            model_name='matierepremiere',
            name='liste',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PPH.liste'),
        ),
    ]