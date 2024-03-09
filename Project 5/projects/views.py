from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


def projects(request):
    page = request.GET.get('page')
    results = 3
    pr = Project.objects.all()
    paginator = Paginator(pr, results)
    try:
        pr = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        pr = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        pr = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5
    if left_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    context = {'projects': pr, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    form = ReviewForm()
    project_obj = Project.objects.get(id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.get_vote_count()

        messages.success(request, 'Your reviews was posted successfully')
        return redirect('project', pk=project_obj.id)

    project_obj = Project.objects.get(id=pk)
    context = {'project': project_obj, 'form': form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.owner = profile
            proj.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    proj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=proj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=proj)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    proj = profile.project_set.get(id=pk)

    if request.method == 'POST':
        proj.delete()
        return redirect('account')

    context = {'project': proj}
    return render(request, 'projects/delete.html', context)