# Generated by Django 4.1.3 on 2022-12-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
