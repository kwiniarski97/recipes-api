# Generated by Django 3.0.2 on 2020-01-31 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_auto_20200131_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='level',
            field=models.CharField(choices=[('VE', 'Bardzo łatwe'), ('E', 'Łatwe'), ('M', 'Średnie'), ('H', 'Trudne'), ('VH', 'Bardzo trudne')], max_length=2),
        ),
    ]
