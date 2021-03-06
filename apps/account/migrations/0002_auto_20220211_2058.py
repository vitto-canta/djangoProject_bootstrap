# Generated by Django 2.2 on 2022-02-11 20:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['-last_login', 'username'], 'permissions': (
                ('search_item', 'can search item'), ('view_item', 'can view an item'),
                ('view_rate', 'can view review rate'), ('be_notified', 'can receive notifications'),
                ('sell_item', 'can sell item'), ('confirm_shipment', 'can confirm shipment'),
                ('get_paid', 'can get paid'),
                ('view_vendor_admin', 'can view vendor admin'), ('read_review', 'can read reviews'),
                ('buy_item', 'can buy item'), ('view_costumer_admin', 'can view costumer admin'),
                ('confirm_delivery', 'can confirm delivery'), ('write_review', 'can write review'),
                ('save_item', 'can save item')), 'verbose_name': 'Accounts', 'verbose_name_plural': 'Accounts'},
        ),
    ]
