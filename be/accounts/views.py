from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserProfile

import requests
from django.conf import settings

def login_view(request):
    return render(request, 'accounts/login.html')

def handle_kakao_callback(request):
    code = request.GET.get('code') # 쿼리 스트링에서 인가 코드 가져오기

    print(f"Auth Code : {code}") # 인가 코드 확인
    
    return redirect('login')
