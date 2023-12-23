from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm, CommentForm

def blog_list(request):
    blogs = Blog.objects.all().order_by('-pub_date')
    return render(request, 'myblog/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'myblog/blog_detail.html', {'blog': blog, 'comment_form': comment_form})

def blog_new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm()
    return render(request, 'myblog/blog_edit.html', {'form': form})
