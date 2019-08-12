from ipware import get_client_ip
from geolite2 import geolite2
import requests
from pprint import pprint

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import RegisterForm, PostForm, EmailForm, CommentForm
from .models import Post, Comment
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
    #ip_adress = get_client_ip(request)
    ip_adress = ('94.188.54.47', True)
    reader = geolite2.reader()
    city = reader.get(ip_adress[0])

    exact_city = city["city"]["names"]['en']

    api_key = '9ed3520438832e7bcaca5088b54d7929'
    code = city['country']['iso_code']
    postal_code = city['postal']['code']

    url = "https://api.openweathermap.org/data/2.5/weather?zip={},{}&units=metric&APPID={}".format(postal_code, code,  api_key)
    r = requests.get(url)

    return render(request, 'blog/my_profile.html', {'ip_adress': ip_adress[0], 'city': exact_city, 'weather': r.json()['main']['temp']})


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


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)




