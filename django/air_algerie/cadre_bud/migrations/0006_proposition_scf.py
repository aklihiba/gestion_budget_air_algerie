# Generated by Django 3.1.5 on 2021-06-25 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0005_proposition_type1'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='scf',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
