from django.db import models
from services.models import Product
from users.models import User
from django.utils.translation import ugettext_lazy as _


class Order(models.Model):
    class Status(models.TextChoices):
        INITIATED = 'i', _('Initiated')
        IN_PROGRESS = 'p', _('In Progress')
        COMPLETED = 'c', _('Completed')
        NOT_COMPLETED = 'n', _('Not Completed')

    class SubStatus(models.TextChoices):
        INITIATED = 'i', _('Initiated')
        ORDER_CONFIRMED = 'oc', _('Order Confirmed')
        PAYMENT_FAILED = 'pf', _('Payment Failed')
        IN_PROGRESS = 'ip', _('In Progress')
        COMPLETED = 'c', _('Completed')
        NOT_COMPLETED = 'n', _('Not Completed')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='order_items')
    payment_done = models.BooleanField(default=False)
    status = models.CharField(
        choices=Status.choices, default=Status.INITIATED,
        max_length=1)
    sub_status = models.CharField(
        choices=SubStatus.choices, default=SubStatus.INITIATED,
        max_length=2)
    payment_json = models.TextField(blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    status_timeline = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
