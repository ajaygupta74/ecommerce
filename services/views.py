import logging
from django.db.models import F, Min, Max
from django.shortcuts import render
from django.views import generic
from project2 import messages

from services.models import (
    Product,
    Order,
    ProductAttribute,
    ProductCategory,
    ProductCategoryFaq,
    ProductReview
)

logger = logging.getLogger(__name__)


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faqs_list = {
            "first": {
                "question": "What is the difference between Nalla neram and \
                gowri Nalla neram?",
                "answer": "The sole distinction between Nalla Neram and Gowri \
                Nalla Neram is that they both employ different timings to \
                determine good and poor times of the day."
            },
            "second": {
                "question": "Which is best Nalla Neram or Gowri Nalla Neram?",
                "answer": "Both Nalla Neram and Gowri Nalla Neram are equally \
                good at evaluating the auspicious timings of the day."
            },
            "third": {
                "question": "Where is Nalla Neram generally followed?",
                "answer": "The majority of south India adheres to Nalla \
                neram. The term 'Nalla neram,' which signifies an excellent \
                or auspicious period, is of Tamil origin."
            },
            "fourth": {
                "question": "In how many time slots is the day divided in \
                Tamil astrology?",
                "answer": "The day is divided into eight equal parts, which \
                are either auspicious or inauspicious."
            },
            "fifth": {
                "question": "Are Nalla Neram's timings accurate?",
                "answer": "Nalla neram timings are based on Tamil astrology, \
                followed chiefly in southern India. Therefore, people \
                consider following Nalla Neram to find good time today and \
                avoid wrong timings, so it is accurate."
            },
            "sixth": {
                "question": "What is the literal meaning of the word Nalla \
                Neram?",
                "answer": "Nalla neram means “good or auspicious time” in its \
                literal sense."
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
        context.update({
            'active_category': category,
            'product_list': product_list.order_by('priority'),
            'faqs': faqs_list
        })
        return context


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
