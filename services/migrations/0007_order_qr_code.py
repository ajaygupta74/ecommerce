# Generated by Django 3.2.7 on 2023-09-25 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_order_payment_reference_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qr_code',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
