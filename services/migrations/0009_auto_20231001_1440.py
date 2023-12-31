# Generated by Django 3.2.7 on 2023-10-01 14:40

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20230927_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='qr_code',
            field=models.FileField(blank=True, null=True, upload_to='uploads/qr_codes/orders/'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='uploads/images/product/product-images/'),
        ),
    ]
