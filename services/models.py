from django.db import models
from sorl.thumbnail import ImageField
from ckeditor.fields import RichTextField


class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    web_description = RichTextField(
        config_name='awesome_ckeditor', null=True, blank=True)
    priority = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE,
        related_name='products')
    web_description = RichTextField(
        config_name='awesome_ckeditor', null=True, blank=True)
    priority = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    likes = models.IntegerField(default=392)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='attributes')
    title = models.CharField(max_length=255, null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0)
    offer_price = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10, default=0)
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class ProductFaq(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product}: {self.question}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True, related_name="images")
    image = ImageField(
        upload_to='upload/images/product/product-images/')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True, related_name="reviews")
    user_name = models.CharField(max_length=255, null=True, blank=True)
    review_msg = models.CharField(max_length=255, null=True, blank=True)
    review_time = models.DateTimeField(null=True, blank=True)
    reply_msg = models.CharField(max_length=255, null=True, blank=True)
    reply_time = models.DateTimeField(null=True, blank=True)
    ratings = models.IntegerField(default=9)
    review_likes = models.IntegerField(default=0)
    review_dislikes = models.IntegerField(default=0)
    reply_likes = models.IntegerField(default=0)
    reply_dislikes = models.IntegerField(default=0)
