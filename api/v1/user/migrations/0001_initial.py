# Generated by Django 2.1.13 on 2020-12-12 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('nick_name', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=64)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]