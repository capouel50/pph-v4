# Generated by Django 4.2.3 on 2023-08-04 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PPH', '0003_alter_supplier_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='postal',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='site',
            field=models.URLField(blank=True),
        ),
    ]
