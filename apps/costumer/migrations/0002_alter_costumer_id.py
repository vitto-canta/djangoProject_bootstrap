# Generated by Django 3.2.12 on 2022-02-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('costumer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
