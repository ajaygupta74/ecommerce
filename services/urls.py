from django.urls import path
from services.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
]