from django.urls import path
from . import views
from social_django.urls import urlpatterns as social_django_urls

urlpatterns = [
    path('login/', views.login_view, name='login'),
]

urlpatterns += social_django_urls # 소셜 인증 URL 포함