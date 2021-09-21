# Generated by Django 3.1.4 on 2021-07-22 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadre_bud', '0045_remove_unite_1_pro'),
    ]

    operations = [
        migrations.CreateModel(
            name='unite_pos6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos6', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.pos6')),
                ('unite', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadre_bud.unite_1')),
            ],
        ),
    ]