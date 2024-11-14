# Generated by Django 4.2 on 2024-11-14 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='restaurant/images/', verbose_name='logotipo')),
                ('description', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('google_link', models.TextField()),
            ],
        ),
    ]