import logging
from django.db.models import F, Min, Max
from django.shortcuts import get_object_or_404, render
from django.views import generic
from project2 import messages

from services.models import (
    Product,
    Order,
    ProductAttribute,
    ProductCategory,
    ProductCategoryFaq,
    ProductReview,
    ProductSubCategory
)

logger = logging.getLogger(__name__)


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faqs_list = {
            "first": {
                "question": ("Is it safe to purchase services for"
                             " various social media platforms?"),
                "answer": ("Yes, our services prioritize security and"
                           " authenticity, ensuring your profiles remain"
                           " safe while you experience growth.")
            },
            "second": {
                "question": ("How long does it take to see results after"
                             " purchasing these services?"),
                "answer": ("You'll notice enhanced engagement and"
                           " visibility within hours, with full delivery"
                           " based on your chosen package.")
            },
            "third": {
                "question": ("Can I target specific demographics or"
                             " regions for my purchased services?"),
                "answer": ("Absolutely. We provide targeting options"
                           " that let you customize your audience to"
                           " match your goals.")
            },
            "fourth": {
                "question": ("Are the followers, likes, and connections"
                             " real people or bots?"),
                "answer": ("We specialize in delivering real, active profiles"
                           " to maintain authenticity and engagement.")
            },
            "fifth": {
                "question": ("Do purchased likes and followers interact with"
                             " my content on these platforms?"),
                "answer": ("While they boost your numbers, engagement"
                           " ultimately depends on the quality and appeal"
                           " of your content.")
            },
            "sixth": {
                "question": ("Is there a satisfaction guarantee or"
                             " refund policy in case I'm not satisfied"
                             " with the service?"),
                "answer": ("We prioritize customer satisfaction and have a"
                           " refund policy outlined in our terms and"
                           " conditions to ensure your peace of mind.")
            },
        }
        product_list = Product.objects.filter(is_active=True)
        context.update({
            'product_list': product_list.order_by('priority'),
            'static_faqs': faqs_list
        })
        return context


class CategoryDetailView(generic.DetailView):
    model = ProductCategory
    template_name = 'home.html'
    queryset = ProductCategory.objects.filter(is_active=True)
    product_queryset = Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        faqs_list = ProductCategoryFaq.objects.filter(
            product_category=category)
        product_list = Product.objects.filter(
            is_active=True,
            category=category)
        sub_category_list = ProductSubCategory.objects.filter(
            products__isnull=False,
            category=category,
            is_active=True)
        context.update({
            'sub_category_list': sub_category_list,
            'active_category': category,
            'product_list': product_list.order_by('priority'),
            'faqs': faqs_list
        })
        return context

    def post(self, request, *args, **kwargs):
        category = self.get_object()
        sel_sub_cat = request.POST.get('sel_sub_cat', '')
        product_list = Product.objects.filter(
            is_active=True,
            category=category)
        if sel_sub_cat:
            product_list = product_list.filter(
                sub_category__slug=sel_sub_cat)
        context = {'product_list': product_list}
        return render(request, 'product_list.html', context)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product_attributes = ProductAttribute.objects.filter(
            product=product).order_by('value')
        product_reviews = ProductReview.objects.filter(
            product=product).order_by('-review_time', '-reply_time')
        min_price_product_attr = ProductAttribute.objects.filter(
                product=product).order_by('offer_price').first()
        context.update({
            'product': product,
            'product_attributes': product_attributes,
            'product_reviews': product_reviews,
            'starting_price': min_price_product_attr.offer_price
        })
        return context


def order_detail(request, category_slug, product_slug):
    template_name = 'order_detail.html'
    category = ProductCategory.objects.filter(slug=category_slug).last()
    product = Product.objects.filter(slug=product_slug).last()
    attr_value = request.GET.get('value', '')
    product_attribute = None
    if attr_value:
        product_attribute = ProductAttribute.objects.filter(
            product=product, value=int(attr_value)).first()
    defaults = {
        'order_price': product_attribute.offer_price,
        'description': 'order_initiated'}
    order, created = Order.objects.update_or_create(
        user=request.user,
        product=product,
        payment_done=False,
        status=Order.Status.INITIATED,
        defaults=defaults)
    context = {
        'product': product,
        'category': category,
        'order': order,
        'input_instructions': messages.PURCHASE_INPUT_INSTRUCTIONS
    }
    return render(request, template_name, context)
