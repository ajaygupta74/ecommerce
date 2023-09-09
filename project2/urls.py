"""project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from project2 import settings
from django.conf.urls.static import static
from users.views import (
    contact_us,
    terms_and_conditions,
    privacy_policy,
    refund_policy,
    ship_and_delivery,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('services/')),
    path('services/', include("services.urls")),
    path('profile/', include("users.urls")),
    path('contactus/', contact_us, name='contact_us'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('refund-policy/', refund_policy, name='refund_policy'),
    path('ship-and-delivery-policy/',
         ship_and_delivery, name='ship_and_delivery'),
    path('terms-and-conditions/',
         terms_and_conditions, name='terms_and_conditions'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
