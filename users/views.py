from django.http import JsonResponse
from django.shortcuts import redirect, render
from services.models import Order
from django.contrib.auth import authenticate, login

from users.models import User


def user_signup(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(phone_number=phone).exists():
            return JsonResponse(
                {'type': 'error',
                 'message': ('This phone number is already registered'
                             ' with another user')})
        elif User.objects.filter(email=email).exists():
            return JsonResponse(
                {'type': 'error',
                 'message': ('This email is already registered'
                             ' with another user')})
        try:
            user = User.objects.create_user(email=email, password=password)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.phone_number = phone
            user.save(update_fields=['first_name',
                                     'last_name',
                                     'phone_number'])
            login(request, user,
                  backend='users.backends.EmailAuthentication')
            return JsonResponse({'type': 'success'})
        except Exception as ex:
            print("Exception occured", ex)
            return JsonResponse({"message": "Try again later"})
    return redirect('/')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user,
                  backend='users.backends.EmailAuthentication')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    return redirect('/')


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
