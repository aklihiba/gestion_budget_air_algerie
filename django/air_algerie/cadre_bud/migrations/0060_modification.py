# Generated by Django 3.1.4 on 2021-07-28 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0059_auto_20210727_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='modification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('type_modif', models.CharField(blank=True, max_length=20, null=True)),
                ('rubrique', models.CharField(blank=True, max_length=20, null=True)),
                ('notifie', models.FloatField(blank=True, null=True)),
                ('modification', models.FloatField(blank=True, null=True)),
                ('cadre1', models.BooleanField(blank=True, default=False)),
                ('monnaie', models.CharField(blank=True, max_length=100, null=True)),
                ('is_valide', models.BooleanField(blank=True, default=False)),
                ('cadre', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cadre3', to='cadre_bud.profile')),
                ('cdd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cdd3', to='cadre_bud.profile')),
                ('pv', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.entete_pv')),
                ('sd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sd3', to='cadre_bud.profile')),
            ],
        ),
    ]
