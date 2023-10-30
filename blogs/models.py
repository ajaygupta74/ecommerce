from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class BlogTag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    class BlogCategory(models.IntegerChoices):
        SERVICES = 0, _('Services')
        HASHTAGFORINSTA = 1, _('Hash tags for insta')

    class Statuschoices(models.IntegerChoices):
        DRAFT = 0, _('Draft')
        PUBLISH = 1, _('Published')

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='uploads/images/blogs/', null=True, blank=True)
    short_content = models.CharField(max_length=255)
    category = models.IntegerField(
        choices=BlogCategory.choices, default=BlogCategory.SERVICES)
    tags = models.ManyToManyField(
        BlogTag, null=True, blank=True, related_name='blog_posts')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='blog_posts',
        on_delete=models.CASCADE)
    content = RichTextField(config_name='awesome_ckeditor')
    status = models.IntegerField(
        default=Statuschoices.PUBLISH, choices=Statuschoices.choices)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.CharField(max_length=500, blank=True)
    seo_json = models.CharField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)
