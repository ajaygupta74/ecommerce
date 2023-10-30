from django.urls import path
from rest_framework.routers import SimpleRouter
from blogs.views import (
    blogListView,
    BlogDetailView,
    # confirm_order_payment
)

service_router = SimpleRouter()

urlpatterns = [
    path('', blogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]
