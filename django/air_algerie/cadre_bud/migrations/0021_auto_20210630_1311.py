# Generated by Django 3.1.5 on 2021-06-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0020_reunion_bud_mois_controle'),
    ]

    operations = [
        migrations.AddField(
            model_name='reunion_bud',
            name='cadre',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='reunion_bud',
            name='cdd',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='reunion_bud',
            name='sd',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
