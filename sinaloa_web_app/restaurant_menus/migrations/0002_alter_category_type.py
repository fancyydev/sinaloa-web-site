# Generated by Django 4.2 on 2024-12-01 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('fria', 'Comida Fria'), ('caliente', 'Comida Caliente'), ('postres', 'Postres'), ('bebidas', 'Bebidas')], max_length=15),
        ),
    ]