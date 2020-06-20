from django.urls import path
from django.contrib.auth import views as auth_view
from member.views import MemberCreate,MemberList,idConfirm,logincheck
urlpatterns = [
    #내장되어있는 로그인 기능에만 적용된다.

    path('login', auth_view.LoginView.as_view(), name = 'login'),
    path('membercreate/', MemberCreate.as_view() , name = 'create'),
    path('logout/', auth_view.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('memberlist/',MemberList.as_view(), name='list'),
    path('membercreate/check/', idConfirm, name='idConfirm'),
    path('logincheck',logincheck , name='logincheck'),
]

