# Generated by Django 4.2.3 on 2024-02-16 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0092_alter_composition_num_formule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parametresformules',
            name='valeur_parametre',
        ),
        migrations.CreateModel(
            name='ParametresDemandes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_demande', models.IntegerField()),
                ('valeur_parametre', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('parametre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PPH.parametresprep')),
            ],
        ),
    ]
