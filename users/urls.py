from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import (
    close_query,
    user_signup,
    user_login,
    user_detail,
)


urlpatterns = [
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='user_login'),
    path('', user_detail, name='user_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    path('close-query/<int:query_pk>/', close_query, name='close_query'),
]
