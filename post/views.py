from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q

def post_index(request):
    # Post modelinden tüm verileri al
    posts = Post.objects.all()

    # Arama sorgusu varsa filtrele
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    # Sayfalama işlemi
    paginator = Paginator(posts, 15)  # Sayfada 15 post göster
    page_number = request.GET.get("page")
    paged_posts = paginator.get_page(page_number)  # Sayfalama için sayfa numarasını al

    # Render işlemi
    return render(request, 'post/index.html', {'posts': paged_posts})


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Kullanıcıyı giriş sayfasına yönlendir

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.slug = slugify(post.title)  # Slug oluşturuluyor
        unique_slug = post.slug
        number = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{post.slug}-{number}"
            number += 1
        post.slug = unique_slug
        post.save()
        messages.success(request, 'Gönderi başarıyla oluşturuldu!')
        return redirect(post.get_absolute_url())
    return render(request, 'post/forms.html', {'form': form})

def post_update(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')  # Kullanıcıyı giriş sayfasına yönlendir

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Gönderi başarıyla güncellendi!')
        return redirect(post.get_absolute_url())
    return render(request, 'post/forms.html', {'form': form})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post  # Burada düzeltme yaptık
        comment.save()
        messages.success(request, 'Yorum başarıyla eklendi!')
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post/detail.html', context)

def post_delete(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')  # Kullanıcıyı giriş sayfasına yönlendir

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Gönderi başarıyla silindi!')
    return redirect('post:index')
