from django.shortcuts import render, get_object_or_404
from .models import Blog

# Create your views here.


def blogs(request):
    blog = Blog.objects.order_by('-date_created')
    return render(request, 'blog/blogs.html', {'blogs': blog})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html', {'blog': blog})