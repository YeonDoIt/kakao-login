from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserProfile

import requests
from django.conf import settings

def login_view(request):
    return render(request, 'accounts/login.html')

def complete_login_view(request):
    kakao_id = request.session.get('kakao_id', 'Unknown')  # 세션에서 카카오 ID 가져오기
    nickname = request.session.get('nickname', 'Guest')      # 세션에서 닉네임 가져오기
    email = request.session.get('email', 'No Email')         # 세션에서 이메일 가져오기

    return render(request, 'accounts/complete_login.html', {
        'kakao_id': kakao_id,
        'nickname': nickname,
        'email': email,
    })

def handle_kakao_callback(request):
    code = request.GET.get('code') # 쿼리 스트링에서 인가 코드 가져오기

    if code:
        try:
            token_data = get_kakao_access_token(code) # 액세스 토큰 요청
            access_token = token_data.get('access_token') # 액세스 토큰 추출

            user_info = get_kakao_user_info(access_token) # 사용자 정보 요청

            return process_user_info(request, user_info) # 사용자 정보 처리 함수 호출
        except Exception as e:
            return render(request, 'error.html', {'error': str(e)})
        
    return redirect('login')

# Access Token 발급
def get_kakao_access_token(code):
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_REST_API_KEY, # 카카오 개발자 콘솔에서 발급받은 REST API 키
        'redirect_uri': settings.KAKAO_REDIRECT_URI, # 리다이렉트 URI
        'code': code, # 쿼리 스트링에서 가져온 인가 코드
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print(f"Access Token: {response.json()}")
        return response.json() # Access Token 반환
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Access Token으로 사용자 정보 가져오기
def get_kakao_user_info(access_token):
    url = "https://kapi.kakao.com/v2/user/me"

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json() # 사용자 정보 반환
    else:
        return Exception(f"Error: {response.status_code}, {response.text}")

# 사용자 정보 처리 함수
def process_user_info(request, user_info):
    # 사용자 정보에서 필요한 데이터 추출
    kakao_id = user_info['id']
    nickname = user_info['properties']['nickname']
    email = user_info.get('kakao_account', {}).get('email', '')

    # 사용자 존재 여부 확인
    user, created = User.objects.get_or_create(
        username=f'kakao_{kakao_id}', # 카카오 id로 사용자 이름 생성
        defaults={
            'email': email, # 이메일 설정
            'first_name': nickname, # 이름 설정
        }
    )

    # UserProfile 생성 또는 업데이터
    UserProfile.objects.get_or_create(user=user, defaults={'usernick': nickname})

    # 로그인 처리
    login(request, user) # Django의 login 함수 사용

    # 세션에 사용자 정보 저장
    request.session['kakao_id'] = kakao_id
    request.session['nickname'] = nickname
    request.session['email'] = email

    return redirect('complete_login') # 로그인 성공 후 리디렉션
