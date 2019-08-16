from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth.views import logout


app_name = "polls"

urlpatterns = [
    #첫번째페이지
    path('form/', views.ProjectCreate, name='form'),
    #두번째페이지
    path('for_form/', views.ReportDailyCreate, name='for_form'),
    path('list/', views.list, name='list'),
    #회원가입
    path('join/', views.signup,  name='join'),
    #로그인
    path('login/', views.signin, name='login'),
    #로그아웃
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    #메인
    path('', views.main, name='main'),
]