# Generated by Django 4.2.3 on 2023-12-13 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0020_alter_typematiere_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matierepremiere',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PPH.typematiere'),
        ),
    ]
