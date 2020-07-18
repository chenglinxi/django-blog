import markdown
from django.core.mail import send_mail
import random
import json
import re
import datetime
import time
from django.views import View
from django.views.generic import ListView
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from Blog.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_HOST_PASSWORD
from front_end import models, forms
from geetest import GeetestLib
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, F
from django.contrib import messages
from utils.send_email import send_email
from notifications.signals import notify


# Create your views here.

# 主页
def home(request):
    article_list = models.Article.objects.filter(is_release=1).order_by('-like_count')
    article_like = models.Article.objects.filter(is_release=1).order_by('-like_count')[0:6]
    article_new = models.Article.objects.filter(is_release=1).order_by('-create_time')[0:6]
    paginator = Paginator(article_list, 10, request=request)  # 实例化Paginator, 每页显示10条数据
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page = paginator.page(page)
    return render(request, 'front_end/home.html', {
        "article_like": article_like,
        "article_new": article_new,
        "page": page,
    })


# 使用滑动验证码
# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 重写登录验证方法，支持账户名和邮箱登录，可扩展其他登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = models.UserInfo.objects.get(Q(username=username) | Q(email=username))  # Q表示或者
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        is_email = re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', username)
        if is_email is None:
            try:
                active = models.UserInfo.objects.get(username=username)
                user = auth.authenticate(username=username, password=pwd)
                if user:
                    # 用户名密码正确
                    # 给用户做登录
                    if active.is_superuser is True:
                        active.is_active = True
                        active.save()
                        auth.login(request, user)
                        ret["msg"] = "/home/"
                    else:
                        if active.is_active is True:
                            auth.login(request, user)
                            ret["msg"] = "/home/"
                        else:
                            ret["status"] = 1
                            ret["msg"] = "用户还没有激活，请您登录邮箱进行激活!"
                else:
                    # 用户名密码错误
                    ret["status"] = 1
                    ret["msg"] = "密码错误！"
            except:
                ret["status"] = 1
                ret["msg"] = "用户名不存在！"
                return JsonResponse(ret)
        else:
            try:
                active = models.UserInfo.objects.get(email=username)
                user = auth.authenticate(username=username, password=pwd)
                if user:
                    # 用户名密码正确
                    # 给用户做登录
                    if active.is_superuser is True:
                        active.is_active = True
                        active.save()
                        auth.login(request, user)
                        ret["msg"] = "/home/"
                    else:
                        if active.is_active is True:
                            auth.login(request, user)
                            ret["msg"] = "/home/"
                        else:
                            ret["status"] = 1
                            ret["msg"] = "用户还没有激活，请您登录邮箱进行激活!"
                else:
                    # 用户名密码错误
                    ret["status"] = 1
                    ret["msg"] = "密码错误！"
            except:
                ret["status"] = 1
                ret["msg"] = "邮箱地址不存在！"
                return JsonResponse(ret)

        # user = auth.authenticate(username=username, password=pwd)
        # try:
        #     active = models.UserInfo.objects.get(username=username)
        #     if user:
        #         # 用户名密码正确
        #         # 给用户做登录
        #         print(4514561651)
        #         if active.is_active is True :
        #             auth.login(request, user)
        #             ret["msg"] = "/home/"
        #         else:
        #             ret["status"] = 1
        #             ret["msg"] = "用户还没有激活，请您登录邮箱进行激活!"
        #     else:
        #         print(111111)
        #         # 用户名密码错误
        #         ret["status"] = 1
        #         ret["msg"] = "密码错误！"
        # except :
        #     pass
        return JsonResponse(ret)

    form_obj = forms.RegForm()
    return render(request, "front_end/login.html", {"form_obj": form_obj})


# 注册
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            user_email = request.POST.get("email", "")
            # 此处加入了邮箱验证的手段
            flag = send_email(user_email, "register")
            if flag == 1:
                form_obj.cleaned_data.pop("re_password")  # 数据库里没有确认密码选项，故删除
                is_active = False
                models.UserInfo.objects.create_user(**form_obj.cleaned_data, is_active=is_active)
                ret["msg"] = "/login/"
                return JsonResponse(ret)
            else:
                ret["msg"] = flag
                ret["status"] = 2
                return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    return render(request, "front_end/register.html", {"form_obj": form_obj})


# 注销账号
def logout(request):
    auth.logout(request)
    return redirect('/home/')


# 忘记密码
def forgot_password(request):
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        is_email = re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', username)
        if is_email is None:
            try:
                models.UserInfo.objects.get(username=username)
                email = models.UserInfo.objects.filter(username=username).values_list('email', flat=True)
                flag = send_email(email[0], "forget")
                if flag == 1:
                    ret["msg"] = "/login/"
                    return JsonResponse(ret)
                else:
                    ret["msg"] = flag
                    ret["status"] = 1
                    return JsonResponse(ret)
            except:
                ret["status"] = 1
                ret["msg"] = "用户名不存在！"
                return JsonResponse(ret)
        else:
            try:
                models.UserInfo.objects.get(email=username)
                flag = send_email(username, "forget")
                if flag == 1:
                    ret["msg"] = "/login/"
                    return JsonResponse(ret)
                else:
                    ret["msg"] = flag
                    ret["status"] = 1
                    return JsonResponse(ret)
            except:
                ret["status"] = 1
                ret["msg"] = "邮箱地址不存在！"
                return JsonResponse(ret)
    return render(request, "front_end/forgot_password.html")


# 校验用户名是否已被注册
def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册，请重新输入！"
    return JsonResponse(ret)


# 邮箱连接验证
class ActiveUserView(View):
    def get(self, request, active_code):
        # 用code在数据库中过滤处信息
        all_records = models.EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # 通过邮箱查找到对应的用户
                user = models.UserInfo.objects.get(email=email)
                if user.is_active == False:
                    # 激活用户
                    user.is_active = True
                    user.save()
                    msg = "用户{}，您的账号激活成功，请转到登录界面进行登录！".format(user.username)
                    return render(request, "front_end/confirm.html", {"msg": msg})
                else:
                    return HttpResponse("你的账号已经激活过了，不需要重新激活，该链接已经失效！")

# 忘记密码，重置密码
def update_password(request, forget_code):
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        User = get_user_model()
        password = request.POST.get("password")
        all_records = models.EmailVerifyRecord.objects.filter(code=forget_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                all_records.delete()
                ret["msg"] = "重置密码成功！"
                ret["status"] = 1
                return JsonResponse(ret)

    all_records = models.EmailVerifyRecord.objects.filter(code=forget_code)
    if all_records:
        return render(request, "front_end/update_password.html", {"forget_code": forget_code})
    else:
        return HttpResponse('该链接已经失效，请重新进入忘记密码界面，从新获取!')

# 文章类比分类显示
def category(request, title):
    title_id = models.Classification.objects.get(title=title)
    article_list = models.Article.objects.filter(classification=title_id, is_release=1).all()
    paginator = Paginator(article_list, 10, request=request)  # 实例化Paginator, 每页显示10条数据
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page = paginator.page(page)
    return render(request, "front_end/article_category.html", {
        "page": page,
    })


#   文章详情页(markdown格式文件)
def article_details(request, pk):
    article_details = models.ArticleDetail.objects.filter(article=pk).first()
    article_details.article.increase_views()
    article_details.content = markdown.markdown(article_details.content.replace("\r\n", '  \n'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ], safe_mode=True, enable_attributes=False)
    # 取出文章评论
    comments = models.Comment.objects.filter(article=pk)
    # 为评论引入表单
    comment_form = forms.CommentForm()

    article_tags = models.Article.objects.get(nid=pk).tags.all()

    # 相邻发表文章的快捷导航(上一页、下一页)
    pre_article = models.Article.objects.filter(nid__lt=article_details.nid).order_by('-nid')
    next_article = models.Article.objects.filter(nid__gt=article_details.nid).order_by('nid')
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None
    return render(request, "front_end/article_details.html", {
        "details": article_details,
        "article_tags": article_tags,
        'pre_article': pre_article,
        'next_article': next_article,
        "comments": comments,
        'comment_form': comment_form,
    })


def author_article(request, pk):
    article_list = models.Article.objects.filter(user=pk, is_release=1).all()
    paginator = Paginator(article_list, 10, request=request)  # 实例化Paginator, 每页显示10条数据
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page = paginator.page(page)
    return render(request, "front_end/author_article.html", {
        "page": page,
    })


def article_data(request, data):
    article_list = models.Article.objects.filter(create_time__year=data[0:4],
                                                 create_time__month=data[-2:], is_release=1).order_by(
        '-create_time').all()
    paginator = Paginator(article_list, 10, request=request)  # 实例化Paginator, 每页显示10条数据
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page = paginator.page(page)
    return render(request, "front_end/article_data.html", {
        "page": page,
    })


# # 评论
# def comment(request, pk):
#     pid = request.POST.get("pid")
#     content = request.POST.get("content")
#     user_id = request.user.pk
#     article_pk = models.Article.objects.get(nid=pk)
#     user_pk = models.UserInfo.objects.get(nid=user_id)
#     response = {}
#     if not pid:  # 根评论
#         models.Comment.objects.create(article=article_pk, user=user_pk, content=content)
#     else:
#         parent_comment = models.Comment.objects.get(nid=pid)
#         models.Comment.objects.create(article=article_pk, user=user_pk, content=content,
#                                       parent_comment=parent_comment)
#
#     return JsonResponse(response)

@csrf_exempt
def article_like(request):
    if request.method == "POST":
        article_id = request.POST.get('article_id')
        ip = request.POST.get('ip')
        user_id = request.user.pk
        if user_id:
            now_user = models.ArticleLike.objects.filter(article_id=article_id).values_list('user_id', flat=True)
            if user_id in now_user:
                ret = {"status": 0, "msg": "你已经赞过了！"}
                return JsonResponse(ret)
            else:
                models.ArticleLike.objects.create(article_id=article_id, user_id=user_id, like_ip=ip)
                models.Article.objects.filter(nid=article_id).update(like_count=F('like_count') + 1)
                ret = {"status": 1, "msg": "成功赞了！"}
                return JsonResponse(ret)
        else:
            now_ip = models.ArticleLike.objects.filter(article_id=article_id).values_list('like_ip', flat=True)
            if ip in now_ip:
                ret = {"status": 0, "msg": "你已经赞过了！"}
                return JsonResponse(ret)
            else:
                models.ArticleLike.objects.create(article_id=article_id, like_ip=ip)
                models.Article.objects.filter(nid=article_id).update(like_count=F('like_count') + 1)
                ret = {"status": 1, "msg": "成功赞了！"}
                return JsonResponse(ret)
    return render(request, 'front_end/home.html')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)


# 搜索
def search_for(request):
    q = request.GET.get('q')
    if q == "" or q == None:
        return redirect('/home/')
    post_list = models.Article.objects.filter(Q(title__icontains=q) | Q(classification__title__icontains=q)
                                              | Q(user__username__icontains=q) |
                                              Q(tags__name__in=[q]),is_release=1).distinct().order_by("-like_count")
    paginator = Paginator(post_list, 10, request=request)  # 实例化Paginator, 每页显示7条数据
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page = paginator.page(page)
    return render(request, 'front_end/results.html', {'page': page})


def article_tag(request, tag):
    # 初始化查询集
    article_list = models.Article.objects.filter(is_release=1).all()
    article_list = article_list.filter(tags__name__in=[tag]).order_by('-create_time')
    paginator = Paginator(article_list, 10, request=request)  # 实例化Paginator, 每页显示7条数据
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page = paginator.page(page)
    return render(request, 'front_end/article_tags.html', {'page': page})


# 评论
def comment(request, pk):
    article = get_object_or_404(models.Article, nid=pk)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.created = datetime.datetime.now()
            new_comment.user = request.user
            pid = request.POST.get("pid")
            # 二级回复
            if pid:
                parent_comment = models.Comment.objects.get(id=pid)
                # 得到目前这是几级回复
                parent_num = parent_comment.level
                if parent_num > 3:
                    # 若回复层级超过四级的，则转换为四级
                    new_comment.parent_id =parent_comment.get_root().id # 返回上一个树节点
                else:
                    new_comment.parent_id = pid
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 增加浏览数
                models.Article.objects.filter(nid=pk).update(comment_count=F("comment_count") + 1)

                # 给其他用户发送通知
                if not parent_comment.user.is_superuser and not parent_comment.user == request.user:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                ret = {"status": 1, "msg": "回复成功！"}
                return JsonResponse(ret)

            new_comment.save()
            # 增加浏览数
            models.Article.objects.filter(nid=pk).update(comment_count=F("comment_count") + 1)

            # 给管理员发送评论通知

            notify.send(
                request.user,
                recipient=article.user,
                verb='评论你的文章',
                target=article,
                action_object=new_comment,
            )

            ret = {"status": 1, "msg": "评论成功！"}
            return JsonResponse(ret)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
