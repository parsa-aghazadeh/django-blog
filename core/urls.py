"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.blog.views import *

urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('posts/create', PostCreate.as_view(),name='post_create'),
    path('posts/<int:post_id>/',PostDetail.as_view(),name='post_detail'),
    path('posts/<int:post_id>/add_comment/',CommentAdd.as_view(), name='add_comment'),
    path('login',Login.as_view(),name='login'),
    path('signup',Register.as_view(),name='signup'),
    path('about',About.as_view(),name='about'),
    path('profile',Profile.as_view(),name='profile'),
    path('logout',Logout.as_view(),name='logout'),
    path('forget_password',ForgetPassword.as_view(),name='forget_password'),
    path('reset_password/<str:token>',ResetPassword.as_view(),name='reset_password'),
    
    
    
    
    path('api/posts',ApiGetAllPosts.as_view()),
    path('api/search',ApiSearch.as_view()),
    path('api/posts/<int:post_id>/like',ApiLike.as_view()),
    path('api/login',ApiLogin.as_view()),
    path('api/profile',ApiProfile.as_view()),
    path('api/post/create',ApiPostCreate.as_view()),
    path('api/logout',Apilogout.as_view()),
    path('api/posts/<int:post_id>/save',ApiSave.as_view()),
    path('api/signup',ApiRegister.as_view()),
    path('api/posts/<int:post_id>/add_comment',ApiCommentAdd.as_view()),
    path('api/post/verify/<int:post_id>',ApiPostVerify.as_view()),

    
]
