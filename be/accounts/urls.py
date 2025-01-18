from django.urls import path
from . import views
from social_django.urls import urlpatterns as social_django_urls

urlpatterns = [
    path('login/', views.login_view, name='login'), # 로그인 화면
    path('handle_kakao_callback/', views.handle_kakao_callback, name='handle_kakao_callback') # 로그인 완료
]

urlpatterns += social_django_urls # 소셜 인증 URL 포함