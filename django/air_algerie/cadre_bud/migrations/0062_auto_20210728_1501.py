# Generated by Django 3.1.4 on 2021-07-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0061_auto_20210728_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modification',
            name='modif',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
