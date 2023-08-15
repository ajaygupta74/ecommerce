from services.models import Product, ProductCategory


def services_category_list(request):
    return {
        'category_list': ProductCategory.objects.filter(
            is_active=True).order_by("priority"),
        'recommended_products': Product.objects.filter(
            is_recommended=True).order_by('priority')
    }
