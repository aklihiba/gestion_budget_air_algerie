# Generated by Django 3.1.5 on 2021-06-29 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0019_auto_20210629_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='reunion_bud',
            name='mois_controle',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
