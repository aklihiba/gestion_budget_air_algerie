# Generated by Django 3.1.5 on 2021-06-24 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entete_pv',
            name='annee',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='entete_pv',
            name='unite',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.unite_1', unique=True),
        ),
    ]
