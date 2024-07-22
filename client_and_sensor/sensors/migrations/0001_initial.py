# Generated by Django 5.0.6 on 2024-06-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
    ]