# Generated by Django 3.1.5 on 2021-06-30 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0021_auto_20210630_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reunion_bud',
            name='statut',
        ),
    ]