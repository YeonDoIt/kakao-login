from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserProfile

def login_view(request):
    return render(request, 'accounts/login.html')

def complete_login(request):
    user = request.user
    if user.is_authenticated:
        # 사용자 프로필이 없다면 생성
        UserProfile.objects.get_or_create(user=user, defaults={
            'usernick': user.username,
            'profile_image': '', # 기본 이미지 처리
        })
        return redirect('home') # 로그인 후 리디렉션할 URL
    return redirect('login')
