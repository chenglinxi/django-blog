"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path, re_path
from django.views.static import serve
from front_end import views
from front_end.views import ActiveUserView
app_name = "front_end"

urlpatterns = [
    path('home/', views.home, name="front_end_home"),
    # 注册于登录
    path("login/", views.login,name="front_end_login"),
    path("register/", views.register, name="front_end_register"),
    path('logout/', views.logout),
    path("forgot_password/", views.forgot_password, name="front_end_forgot_password"),
    # 专门用来校验用户名是否已被注册的接口
    path('check_username_exist/', views.check_username_exist),
    # 用来验证邮箱连接是否被激活
    re_path(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),  # 提取出active后的所有字符赋给active_code
    # 用来找回密码
    re_path(r'^update_password/(?P<forget_code>.*)/$', views.update_password, name="front_end_update_password"),

    # 极验滑动验证码 获取验证码的url
	path('pc-geetest/register', views.get_geetest),
    # 文章类
    re_path(r'^article_category/(\w+)/', views.category),
	re_path(r'^acticle_details/(\d+)/', views.article_details, name="article_detail"),
	re_path(r'^author/(\w+)/', views.author_article),
	re_path(r'^article_data/(.*)/', views.article_data),
    re_path(r'^article_tag/(.*)/', views.article_tag),
	path('article_like/',views.article_like),
	path('search_for/',views.search_for),
    # 发表评论
    re_path('comment/(\d+)/', views.comment,),
]