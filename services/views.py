from datetime import datetime, timezone
import logging
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic
from project2 import messages
from project2.slack import send_slack_notification
from services.helpers import generate_qr_code
from django.core.files.storage import default_storage

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
    template_name = 'services/home.html'

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
    template_name = 'services/home.html'
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
            is_active=True).distinct()
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
        return render(request, 'services/product_list.html', context)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "services/product_detail.html"

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
    template_name = 'services/order_detail.html'
    category = ProductCategory.objects.filter(slug=category_slug).last()
    product = Product.objects.filter(slug=product_slug).last()
    order_id = request.GET.get('order_id', '')
    order = None
    if order_id:
        order = Order.objects.filter(pk=order_id).first()
        if order.qr_code:
            default_storage.delete(order.qr_code.name)
        generate_qr_code(order)

    if request.method == 'POST':
        order_action = request.POST.get('order_action', '')
        if order_action == 'confirm_payment':
            user_input_text = request.POST.get('user_input_text', '')
            user_message = request.POST.get('user_message', '')
            if order and user_input_text:
                order.status = Order.Status.IN_PROGRESS
                order.sub_status = Order.SubStatus.IN_PROGRESS
                order.payment_json.update({
                    'user_input_text': user_input_text,
                    'user_message': user_message})
                order.save(update_fields=['order_price',
                                          'status',
                                          'sub_status',
                                          'payment_json'])
                current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                order_time = datetime.strftime(current_time, "%d-%m-%Y %H:%M")
                sl_message = messages.ORDER_PURCHASED_MSG.format(
                    USER=order.user,
                    PRODUCT=order.product,
                    AMOUNT=order.order_price,
                    TIME=order_time,
                    ORDER_ID=order.pk,
                    ORDER_SLUG=order.slug,
                    USER_INPUT_TEXT=order.payment_json.get('user_input_text'))
                send_slack_notification('order-purchased', sl_message)
                return redirect('/profile/')

        attr_id = request.POST.get('attr_id', '')
        order_price = request.POST.get('order_price', '')
        product_attribute = None
        product_attribute = ProductAttribute.objects.filter(
            product=product, pk=int(attr_id)).first()
        defaults = {
            'order_price': float(order_price),
            'description': f'{product.title}',
            'payment_json': {
                'product_attr_id': attr_id,
                'value': f'{product_attribute.value}'}}
        if not order_price and product_attribute:
            defaults['order_price'] = product_attribute.offer_price
        order, created = Order.objects.update_or_create(
            user=request.user,
            product=product,
            payment_done=False,
            status=Order.Status.INITIATED,
            defaults=defaults)
        response_data = {
            'status': 'success',
            'order_id': order.id}
        return JsonResponse(response_data)
    context = {
        'product': product,
        'category': category,
        'order': order,
    }
    return render(request, template_name, context)
