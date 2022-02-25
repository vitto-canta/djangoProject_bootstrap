# Generated by Django 2.2 on 2022-02-10 15:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
        ('costumer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=250)),
                ('rate', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5),
                                                                    django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('addressed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews',
                                                   to='vendor.Vendor')),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='costumer.Costumer')),
            ],
        ),
    ]