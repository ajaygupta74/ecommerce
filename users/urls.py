from django.urls import path
from users.views import (
    user_detail
)


urlpatterns = [
    path('', user_detail, name='user_detail'),
]
