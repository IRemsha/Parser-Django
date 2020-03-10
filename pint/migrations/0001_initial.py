# Generated by Django 2.2.7 on 2019-11-23 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectOldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=350)),
                ('price', models.IntegerField()),
                ('square_all', models.IntegerField()),
                ('square_kitchen', models.IntegerField()),
                ('square_live', models.IntegerField()),
                ('url', models.CharField(max_length=400, unique=True)),
                ('last_seen', models.IntegerField(default=0)),
                ('ad_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pint.AdType')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pint.City')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pint.Floor')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pint.Material')),
                ('object_old_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='pint.ObjectOldType')),
                ('object_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pint.ObjectType')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pint.Room')),
            ],
        ),
    ]