from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django_recaptcha.fields import ReCaptchaField

class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Yazar', related_name='posts')
    title = models.CharField(max_length=120, verbose_name="Başlık")
    content = RichTextField(verbose_name="Metin")
    publishingday = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('post:create')

    def get_update_url(self):
        return reverse('post:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'slug': self.slug})

    def get_index_url(self):
        return reverse('post:index')

    def save(self, *args, **kwargs):
        # Ensure the slug is unique
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            number = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{number}"
                number += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-publishingday', 'id']

class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Isim')
    content = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)