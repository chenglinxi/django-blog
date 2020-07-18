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
from back_end import views


urlpatterns = [
    path('index/', views.index),
    path('welcome/', views.welcome),
    path('article_list/', views.article_list),
    path('article_class/', views.article_class),
    re_path(r'^article_class_edit/(\w+)/', views.article_class_edit),
    path('all_article/', views.all_article),
    path('user_article/', views.user_article),
    path('user_article_release/', views.user_article_release),
    path('user_article_draft/', views.user_article_draft),
    path('user_article_review/', views.user_article_review),
    path('user_article_recycle/', views.user_article_recycle),
    path('release_draft/',views.release_draft),
    path('draft_recycle/', views.draft_recycle),
    path('draft_review/', views.draft_review),
    path('recycle_draft/', views.recycle_draft),
    path('recycle_delete/', views.recycle_delete),
	re_path('review_view/(\d+)/', views.review_view),
    path('review_yes/', views.review_yes),
    path('review_no/', views.review_no),
    path('article_class_delete/', views.article_class_delete),
    path('article_class_add/', views.article_class_add),
    path('article_add/', views.article_add),
    path('article_add_review/', views.article_add_review),
    re_path('article_updata_details/(\d+)/', views.article_updata_details),
    path('comment_list/', views.comment_list),
    re_path('comment_update/(\d+)/',views.comment_update),
    path('comment_del/', views.comment_del),
    path('comment_all_del/', views.comment_all_del),
    path('admin_index/', views.admin_index),
    path('admin_list/', views.admin_list),
    path('user_is_superuser/',views.user_is_superuser),
    path('user_del/',views.user_del),
    path('user_all_del/',views.user_all_del),
    path('admin_updata_details/', views.admin_updata_details),
    path('admin_ad_poster/', views.admin_ad_poster),
    path('ad_poster_add/', views.ad_poster_add),
    re_path('ad_poster_update/(\d+)/', views.ad_poster_update),
    path('ad_poster_del/', views.ad_poster_del),
    path('ad_poster_all_del/', views.ad_poster_all_del),
    path('ad_poster_is_show/', views.ad_poster_is_show),
    path('links/', views.links),
    path('links_add/',views.links_add),
    re_path('links_update/(\d+)/',views.links_update),
    path('links_is_show/',views.links_is_show),
    path('links_del/',views.links_del),
    path('links_all_del/',views.links_all_del),

    # 博客内容上传图片
    path('api-upload-url/', views.api_upload_url),
    # 预览文章
    re_path('article_view/(\d+)/', views.article_view),

]