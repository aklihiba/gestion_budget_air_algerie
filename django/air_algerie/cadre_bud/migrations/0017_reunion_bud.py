# Generated by Django 3.1.5 on 2021-06-29 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0016_auto_20210629_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='reunion_bud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('statut', models.IntegerField(blank=True, null=True)),
                ('controle_budgetaire', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.controle_bud')),
                ('proposition', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.proposition')),
            ],
        ),
    ]
