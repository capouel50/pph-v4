# Generated by Django 4.2.3 on 2024-01-23 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0054_conditionnement'),
    ]

    operations = [
        migrations.AddField(
            model_name='matierepremiere',
            name='cdt',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PPH.conditionnement'),
            preserve_default=False,
        ),
    ]
