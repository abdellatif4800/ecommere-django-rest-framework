# Generated by Django 5.2.4 on 2025-07-17 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
