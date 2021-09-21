# Generated by Django 3.1.5 on 2021-06-28 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0009_remove_proposition_calcul'),
    ]

    operations = [
        migrations.CreateModel(
            name='entete_controle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(blank=True, null=True)),
                ('unite', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.unite_1')),
            ],
        ),
        migrations.CreateModel(
            name='controle_budgetaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('rubrique', models.CharField(blank=True, max_length=20, null=True)),
                ('mois', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('montant', models.FloatField(blank=True, null=True)),
                ('type1', models.CharField(blank=True, max_length=20, null=True)),
                ('scf', models.IntegerField(blank=True, null=True)),
                ('rempli', models.BooleanField(blank=True, default=True)),
                ('ec', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.entete_controle')),
            ],
        ),
    ]