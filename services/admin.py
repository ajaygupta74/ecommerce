from django.contrib import admin


from services.models import (
    Order,
    ProductCategory,
    ProductSubCategory,
    Product,
    ProductAttribute,
    ProductCategoryFaq,
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
    search_fields = ('title', )


class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active']
    search_fields = ('title', )


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'title', 'value', 'price', 'offer_price',
        'is_recommended', 'is_active']
    autocomplete_fields = ('product', )


class ProductFaqAdmin(admin.ModelAdmin):
    list_display = ['product', 'question', 'answer']
    autocomplete_fields = ('product', )


class ProductCategoryFaqAdmin(admin.ModelAdmin):
    list_display = ['product_category', 'question', 'answer']
    autocomplete_fields = ('product_category', )


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_approved']
    autocomplete_fields = ('product', )


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'first_name', 'last_name', 'ratings', 'review_likes',
        'review_dislikes', 'reply_likes', 'reply_dislikes']
    autocomplete_fields = ('product', )


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'product', 'payment_done', 'status', 'sub_status',
        'created_at', 'updated_at']
    list_filter = (
        'status', 'status', 'sub_status', 'created_at', 'updated_at'
    )
    search_fields = ('user__email', 'user__phone_number', 'product__title')
    autocomplete_fields = ('user', 'product')
    readonly_fields = ('slug', )


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductFaq, ProductFaqAdmin)
admin.site.register(ProductCategoryFaq, ProductCategoryFaqAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
