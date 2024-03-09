from django.db import models
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назваание')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')
    content = models.TextField(blank=True, verbose_name='Содержимое')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='Изображение')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_created']


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'