# Generated by Django 2.1.2 on 2018-11-01 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminDashboard', '0012_auto_20181101_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinventory',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='inventory_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='AdminDashboard.ProductInventory'),
            preserve_default=False,
        ),
    ]