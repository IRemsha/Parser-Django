# Generated by Django 2.2.7 on 2020-02-17 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pint', '0004_auto_20200217_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='object_old_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pint.ObjectOldType'),
        ),
    ]
