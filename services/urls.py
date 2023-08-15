from django.urls import path
from rest_framework.routers import SimpleRouter
from services.views import (
    HomeView,
    CategoryDetailView,
    ProductDetailView
)

service_router = SimpleRouter()
service_router.register(r'', HomeView, basename='service_home')

urlpatterns = [
    path('', HomeView.as_view(), name='service_home'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/',
         ProductDetailView.as_view(),
         name='product_detail')
]
