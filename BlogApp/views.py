from django.shortcuts import render
import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm

# Create your views here.
def bloghome(request):
    blogs = Blog.objects.order_by('-pub_date')[:5]
    return render(request, 'BlogApp/bloghome.html', {'blogs': blogs})

#hasnt been implemented yet
def blogindex(request):
    return render(request, 'BlogApp/blogindex.html')

def blog(request):
    return render(request, 'BlogApp/blog.html' )

#organization section
def organization(request):
    return render(request, 'BlogApp/organization.html' )

def philosophy(request):
    return render(request, 'BlogApp/philosophy.html')

def blogvandeweekahmattie(request):
    return render(request, 'BlogApp/blog-1.html')

def dragonfrog(request):
    return render(request, 'BlogApp/dragonfrog.html')

#crud
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'BlogApp/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'BlogApp/blog_detail.html', {'blog': blog})

def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('blog-list')
    else:
        form = BlogForm()
    return render(request, 'BlogApp/blog_form.html', {'form': form})

def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('blog-detail', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'BlogApp/blog_form.html', {'form': form})

def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('blog-list')
def home(request):
    return render(request, 'BlogApp/home.html' )
