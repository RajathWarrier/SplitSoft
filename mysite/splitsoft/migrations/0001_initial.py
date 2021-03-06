# Generated by Django 3.2.4 on 2021-06-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Owes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who_FName', models.CharField(max_length=20)),
                ('who_LName', models.CharField(max_length=20)),
                ('whom_FName', models.CharField(max_length=20)),
                ('whom_LName', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fName', models.CharField(max_length=20)),
                ('lName', models.CharField(max_length=20)),
                ('groups', models.ManyToManyField(to='splitsoft.Group')),
            ],
        ),
    ]
