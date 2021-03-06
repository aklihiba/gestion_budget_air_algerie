# Generated by Django 3.2.5 on 2021-07-11 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0029_auto_20210630_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='realisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('controle_budgetaire', models.FloatField(blank=True, null=True)),
                ('cloture', models.FloatField(blank=True, null=True)),
                ('prevision', models.FloatField(blank=True, null=True)),
                ('mois_controle', models.CharField(blank=True, max_length=20, null=True)),
                ('cadre1', models.BooleanField(blank=True, default=False)),
                ('cadre', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cadre2', to='cadre_bud.profile')),
                ('cdd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cdd2', to='cadre_bud.profile')),
                ('proposition', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.proposition')),
                ('sd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sd2', to='cadre_bud.profile')),
            ],
        ),
        migrations.CreateModel(
            name='actualisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('controle_budgetaire', models.FloatField(blank=True, null=True)),
                ('cloture', models.FloatField(blank=True, null=True)),
                ('prevision', models.FloatField(blank=True, null=True)),
                ('mois_controle', models.CharField(blank=True, max_length=20, null=True)),
                ('cadre1', models.BooleanField(blank=True, default=False)),
                ('cadre', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cadre1', to='cadre_bud.profile')),
                ('cdd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cdd1', to='cadre_bud.profile')),
                ('proposition', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.proposition')),
                ('sd', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sd1', to='cadre_bud.profile')),
            ],
        ),
    ]
