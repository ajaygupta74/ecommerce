from django.contrib import admin

from blogs.models import Blog, BlogTag


class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'updated_at', 'created_at']
    readonly_fields = ('author', )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(BlogTag, BlogTagAdmin)
admin.site.register(Blog, BlogAdmin)
