from django.shortcuts import render

from payments.models import Order


def user_detail(request):
    template = 'user_detail.html'
    user = request.user
    orders = Order.objects.filter(user=user)
    completed_orders = orders.filter(status=Order.Status.COMPLETED)
    inprogress_orders = orders.exclude(
        pk__in=[order.pk for order in completed_orders])
    context = {
        'completed_orders': completed_orders,
        'inprogress_orders': inprogress_orders
    }
    return render(request, template, context)
