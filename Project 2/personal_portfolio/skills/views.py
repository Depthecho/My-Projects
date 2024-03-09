from django.shortcuts import render
from .models import Skill

# Create your views here.


def index(request):
    skills = Skill.objects.all()
    return render(request, 'skills/index.html', {'skills': skills})