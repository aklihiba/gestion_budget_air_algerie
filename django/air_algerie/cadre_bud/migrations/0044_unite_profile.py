# Generated by Django 3.1.4 on 2021-07-22 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0043_notifie_bud_m'),
    ]

    operations = [
        migrations.CreateModel(
            name='unite_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.profile')),
                ('unite', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.unite_1')),
            ],
        ),
    ]
