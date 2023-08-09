from django.contrib import admin


from services.models import (
    ProductCategory,
    Product,
    ProductAttribute,
    ProductFaq,
    ProductImage,
    ProductReview
)


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'priority', 'is_active', 'likes', 'dislikes']
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', )


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active']


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'title', 'value', 'price', 'offer_price',
        'is_recommended', 'is_active']
    autocomplete_fields = ('product', )


class ProductFaqAdmin(admin.ModelAdmin):
    list_display = ['product', 'question', 'answer']
    autocomplete_fields = ('product', )


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_approved']
    autocomplete_fields = ('product', )


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'user_name', 'ratings', 'review_likes', 'review_dislikes',
        'reply_likes', 'reply_dislikes']
    autocomplete_fields = ('product', )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductFaq, ProductFaqAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
