# Generated by Django 3.1.5 on 2021-06-24 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0003_auto_20210624_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='proposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('rubrique', models.CharField(blank=True, max_length=20, null=True)),
                ('calcul', models.FloatField(blank=True, null=True)),
                ('cloture', models.FloatField(blank=True, null=True)),
                ('prevision', models.FloatField(blank=True, null=True)),
                ('pv', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.entete_pv')),
            ],
        ),
    ]