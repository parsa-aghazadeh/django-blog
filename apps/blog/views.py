from typing import Any
from django.shortcuts import render, redirect
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from datetime import date, datetime
from django.views import generic, View
from django.conf import settings
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q, Count, Sum, F
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError
import json
import re
import random
import string


class Index(View):
    def get(self, request):
        # send_mail(
        #     "title test password",
        #     "email content",
        #     settings.EMAIL_FROM,
        #     ["8parsa3@gmail.com"],
        #     False,
        # )
        if "q" in request.GET:
            if request.user.is_authenticated and request.user.role == int(User.Roles.ADMIN):
                posts = Post.objects.filter(Q(content__contains=request.GET['q']) | Q(title__contains=request.GET['q']))
            else:
                posts = Post.objects.filter(Q(content__contains=request.GET['q']) | Q(title__contains=request.GET['q']),
                                            verified=1)
            context = {
                "posts": posts
            }
            return render(request, "index.html", context)
        else:
            if request.user.is_authenticated and request.user.role == int(User.Roles.ADMIN):
                posts = Post.objects.all()

            else:
                posts = Post.objects.filter(verified=1)
            context = {
                "posts": posts
            }
            return render(request, "index.html", context)


class Profile(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {
            "username": request.user,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }

        return render(request, 'profile.html', context)


class PostCreate(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'create_post.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        # dirty_data = request.POST.dict()
        form = PostFrom(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user
            data['created_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(data)
            Post.objects.create(**data)

        return redirect('index')


class PostDetail(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)
        context = {
            'post': post,
            'comments': comments,
            'commentable': request.user.is_authenticated
        }
        return render(request, 'post_detail.html', context)


class CommentAdd(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return redirect('login')
        post = Post.objects.get(pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['post'] = post
            data['user'] = request.user
            Comment.objects.create(**data)
        else:
            form = CommentForm()
        return redirect('post_detail', post_id=post.pk)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                login(request, user)
                return redirect('index')
        messages.success(request, 'The password or username entered is incorrect')
        return render(request, 'login.html')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class Register(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == data['password_confirmation']:
                try:
                    user = User.objects.create_user(username=data["username"], password=data["password"],
                                                    email=data["email"])
                except IntegrityError as e:
                    if e.args[0] == 1062:
                        messages.success(request, 'User exists, please login')
                        return render(request, 'signup.html')
                    return HttpResponse('An error occurred')
                messages.success(request, f'Dear {data["username"]} you have successfully registered')
                # messages.add_message(request,messages.INFO,f'Dear {data["username"]} you have successfully registered')
                return redirect('index')
            else:
                messages.success(request, 'password does not mach')
                return render(request, 'signup.html')
        return render(request, 'signup.html')


class About(View):
    def get(self, reguest):
        return render(reguest, 'about.html')


class ForgetPassword(View):
    def get(self, request):
        return render(request, 'forget_password.html')

    def post(self, request):
        input_value = request.POST.get('input_field')

        username_pattern = r'^[a-zA-Z0-9_]+$'
        if re.match(username_pattern, input_value):
            user = User.objects.get(username=input_value)
            if user and user.email is not None:
                random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
                user.token = random_string
                user.save()
                print(
                    f"hi dear {user.username}",
                    f"to reset password click on the link : http://0.0.0.0:8000/reset_password/{user.token}",
                )
                return HttpResponse("ورودی یک نام کاربری معتبر است")
            return HttpResponse('با نام کاربری وارد شده کاربری یافت نشد')
        else:
            try:
                validate_email(input_value)
                user = User.objects.get(email=input_value)
                if user:
                    random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
                    user.token = random_string
                    user.save()
                    send_mail(
                        f"hi dear {user.username}",
                        f"to reset password click on the link : https://0.0.0.0:8000/reset_password/{user.token}",
                        settings.EMAIL_FROM,
                        ["8parsa3@gmail.com"],
                        False,
                    )
                    return HttpResponse("ورودی یک ایمیل معتبر است")
                return HttpResponse('با ایمیل وارد شده کاربری یافت نشد')
            except EmailNotValidError:
                return HttpResponse("ورودی نامعتبر است.")


class ResetPassword(View):
    def get(self, request, token):
        user = User.objects.get(token=token)
        if user:
            login(request, user)
            context = {'token': token}
            return render(request, 'reset_password.html', context)

    def post(self, request, token):
        data = request.POST
        if data['password'] == data['password_confirmation']:
            user = User.objects.get(username=request.user)
            user.set_password(data['password'])
            user.save()
            messages.success(request, f'your password changed')
            return redirect('login')


# --------------------------------        
# --------------------------------
# API endpoints starting from here 
# --------------------------------
# --------------------------------


class ApiRegister(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == data['password_confirmation']:
                try:
                    user = User.objects.create_user(username=data["username"], password=data["password"],
                                                    email=data["email"])
                    return JsonResponse({"message": "registerd"})
                except IntegrityError as e:
                    if e.args[0] == 1062:
                        return JsonResponse({"messages": "user exists"}, status=409)
                    return JsonResponse({'message': 'an error occurred'}, status=500)
            else:
                return JsonResponse({"message": "password does not match"})
        else:
            return JsonResponse({"message": form.errors})


class ApiPostCreate(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"message": "user is not lagged"})
        form = PostFrom(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user
            data['created_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if request.user.role == int(User.Roles.ADMIN):
                data['verified'] = True
            Post.objects.create(**data)
            return JsonResponse({"message": "The post created successfully"})
        else:
            return JsonResponse({"message": "form is not valid", "errors": form.errors})


class ApiCommentAdd(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return JsonResponse({"message": "user is not lagged"})
        post = Post.objects.get(pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['post'] = post
            data['user'] = request.user
            Comment.objects.create(**data)
            return JsonResponse({"message": "comment added"})
        else:
            return JsonResponse({"message": "form is not valid", "errors": form.errors})


class ApiProfile(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"message": "user is not lagged"})
        context = {
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }
        return JsonResponse(context)


class ApiLogin(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                login(request, user)
                context = {"message": "logged in"}
                return JsonResponse(context)
            else:
                error = {"error": "The password or username entered is incorrect"}
                return JsonResponse(error, status=403)
        else:
            error = {"error": "form is invalid"}
            return JsonResponse(error, status=400)


class Apilogout(View):
    def get(self, request):
        logout(request)
        return JsonResponse({"message": "user logged out"})


class ApiLike(View):
    def get(self, request, post_id):
        try:
            # todo : check user is authenticated
            post = Post.objects.get(pk=post_id)
            total_likes = post.likes.count()
            context = {"total_likes": total_likes}
            return JsonResponse(context)
        except Post.DoesNotExist:
            error = {"error": "Post not found"}
            return JsonResponse(error, status=404)

    def post(self, request, post_id):

        if request.user.is_authenticated:
            try:
                user = request.user
                post = Post.objects.get(pk=post_id)
                if user in post.likes.all():
                    post.likes.remove(user)
                    total_likes = post.likes.count()
                    context = {"total_likes": total_likes,
                               "like_status": 'disliked'}
                    return JsonResponse(context)
                else:
                    post.likes.add(user)
                    total_likes = post.likes.count()
                    context = {"total_likes": total_likes,
                               "like_status": 'liked'}
                    return JsonResponse(context)
            except Post.DoesNotExist:
                error = {"error": "Post not found"}
                return JsonResponse(error, status=404)
        else:
            error = {"error": "You must be logged in."}
            return JsonResponse(error, status=401)


class ApiSave(View):

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        total_save = post.saved.count()
        return JsonResponse({"total_save": total_save})

    def post(self, request, post_id):
        try:
            if request.user.is_authenticated:
                user = request.user
                post = Post.objects.get(pk=post_id)
                if user in post.saved.all():
                    post.saved.remove(user)
                    total_save = post.saved.count()
                    return JsonResponse({"save_status": " unsaved", "total_save": total_save})
                else:
                    post.saved.add(user)
                    total_save = post.saved.count()
                    return JsonResponse({"save_status": "saved", "total_save": total_save})
            else:
                return JsonResponse({"message": "your not logged in"}, status=401)
        except:
            return JsonResponse({"message": "error"}, status=500)


class ApiGetAllPosts(View):
    def get(self, request):
        posts = Post.objects.filter(verified=1).annotate(
            short_content=F('content')[:100]
        ).values('title', 'id', 'short_content')
        print(posts.query)
        context = {"posts": list(posts)}
        return JsonResponse(context)


class ApiSearch(View):
    def get(self, request):
        if "q" in request.GET:
            posts = Post.objects.filter(
                Q(content__contains=request.GET['q']) | Q(title__contains=request.GET['q'])).values('title', 'id')
            if not posts:
                return JsonResponse({"message": "sorry no result"}, status=204)
            context = {"posts": list(posts)}
            return JsonResponse(context)
        else:
            return JsonResponse({"message": "sorry no result"}, status=204)



class ApiPostVerify(View):
    def post(self, request, post_id):
        if request.user.is_authenticated and request.user.role == int(User.Roles.ADMIN):
            post = Post.objects.get(pk=post_id)
            post.verified = 1
            post.save()
            return JsonResponse({"message": f"The post with title `{post.title}` verified"})
        else:
            return JsonResponse({"message": "You are not logged in"}, status=401)

