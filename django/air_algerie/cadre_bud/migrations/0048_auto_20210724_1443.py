# Generated by Django 3.1.4 on 2021-07-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0047_auto_20210722_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='ajouter_par',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proposition',
            name='date_ajout',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proposition',
            name='date_modif',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proposition',
            name='modifier_par',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
