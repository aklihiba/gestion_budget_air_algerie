# Generated by Django 3.1.4 on 2021-07-25 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0050_auto_20210724_2341'),
    ]

    operations = [
        migrations.CreateModel(
            name='historique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('type_1', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('date_ajout', models.CharField(blank=True, max_length=100, null=True)),
                ('date_modif', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
