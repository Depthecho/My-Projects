from django import template
from django.db.models import Avg
from mainpage.models import ProductComment


register = template.Library()


@register.simple_tag
def calculate_average_rating(product_id):
    average_rating = ProductComment.objects.filter(product_id=product_id).aggregate(Avg('rating'))['rating__avg']
    return average_rating or 0