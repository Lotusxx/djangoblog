from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

from django.contrib.contenttypes.models import ContentType

#実行順１
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.slug:
            return reverse('post_list_by_category', args=[self.slug])
        else:
            return reverse('post_list_by_category', args=['undefined'])
#実行順２
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == apps.get_app_config('djangoblog').name:
        category, created = Category.objects.get_or_create(
            name='未分類',
            slug='undefined',
            defaults={
                'description': 'Default category created by migration',
            }
        )
        ContentType.objects.clear_cache()

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, related_name='posts', default=1) #実行順３

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50, blank=True, default='匿名')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text
