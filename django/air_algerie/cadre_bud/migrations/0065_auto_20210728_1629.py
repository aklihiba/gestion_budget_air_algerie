# Generated by Django 3.1.4 on 2021-07-28 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0064_historique_modification'),
    ]

    operations = [
        migrations.AddField(
            model_name='historique_modification',
            name='date1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historique_modification',
            name='date2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='historique_modification',
            name='date3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='modification',
            name='date1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='modification',
            name='date2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='modification',
            name='date3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
