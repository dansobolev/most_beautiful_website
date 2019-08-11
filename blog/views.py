import requests
from bs4 import BeautifulSoup

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import RegisterForm, PostForm, EmailForm
from .models import Post
from django.core.mail import send_mail
from django.contrib.auth.models import User





def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        print("POST")
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            post.published_date = timezone.now()
            #name = form.cleaned_data.get("author")
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        print("NOT POST")
    return render(request, 'blog/post_edit.html', {'form': form, "post": post})



def register(request):
    if request.method == "POST":
        print("POST")
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        print("NOT POST")
        form = RegisterForm()

    return render(request, 'register/register.html', {"form": form})





def yourprofile(request):
    url = 'https://whoer.net/'
    page = requests.get(url)
    # page.status_code (если выведит 200, значит страница успешно загружена)


    soup = BeautifulSoup(page.text, 'html.parser')
    ip_adress = soup.find_all('strong')[0].get_text()
    ip_adress = ip_adress.strip()

    return render(request, 'blog/my_profile.html', {'ip_adress': ip_adress})


def password_res(req):
    return render(req, 'registration/password_reset_form.html')

def send_email_function(name, email, text, user):
    # user_email можешь сохранить только для того чтоб после отсылать обратно
    send_mail(
        'Name: {}'.format(name),
        'Message: {}\nEmail: {}\nUsername: {}'.format(text, email, user),
        'forum.staff01@gmail.com',
        ['forum.staff01@gmail.com']
    )



def contact_us(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            send_email_function(name, email, message, user)
            return render(request, 'blog/sent_successfully.html')

    else:
        form = EmailForm()
        print("NOT POST")

    return render(request, 'blog/contact.html', {'form ': form})


def test_user_page(request):
    return render(request, 'blog/test_user_page.html')





