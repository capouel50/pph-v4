# Generated by Django 4.2.3 on 2023-12-12 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0017_alter_matierepremiere_fournisseur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matierepremiere',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPH.supplier'),
        ),
    ]
