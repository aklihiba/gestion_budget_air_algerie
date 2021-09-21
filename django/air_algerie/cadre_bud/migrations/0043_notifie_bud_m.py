# Generated by Django 3.1.4 on 2021-07-22 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0042_auto_20210719_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='notifie_bud_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('rubrique', models.CharField(blank=True, max_length=20, null=True)),
                ('prevision', models.FloatField(blank=True, null=True)),
                ('mois', models.CharField(blank=True, max_length=100, null=True)),
                ('cadre1', models.BooleanField(blank=True, default=False)),
                ('monnaie', models.CharField(blank=True, max_length=100, null=True)),
                ('cadre', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cadre2', to='cadre_bud.profile')),
                ('cdd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cdd2', to='cadre_bud.profile')),
                ('pv', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.entete_pv')),
                ('sd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sd2', to='cadre_bud.profile')),
            ],
        ),
    ]
