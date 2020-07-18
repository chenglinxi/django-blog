from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from datetime import datetime
# Django-taggit
from taggit.managers import TaggableManager


# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10,
                                 choices=(("register", u"注册"), ("forget", u"找回密码")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Classification(models.Model):
    """
    文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  # 分类标题

    def __str__(self):
        return self.title


class Label(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    tags = TaggableManager()  # 标签
    article_id = models.OneToOneField(to="Article", to_field="nid", on_delete=models.CASCADE, null=True)


class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')  # 文章标题
    desc = models.CharField(max_length=255, verbose_name='文章摘要')  # 文章摘要
    create_time = models.DateTimeField(verbose_name='创建时间')  # 创建时间
    cover_photo = models.FileField(upload_to="cover_photo/", default="cover_photo/default.png", verbose_name="封面图片")
    is_draft = models.IntegerField(verbose_name='是否为草稿', default=1)
    is_review = models.IntegerField(verbose_name='是否审核', default=0)
    is_release = models.IntegerField(verbose_name='是否发布', default=0)
    is_recycle = models.IntegerField(verbose_name="是否在回收站", default=0)
    browse_count = models.IntegerField(verbose_name='浏览数', default=0)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    like_count = models.IntegerField(verbose_name='喜欢数', default=0)
    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.CASCADE)
    classification = models.ForeignKey(to="Classification", to_field="nid", on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name="阅读数")
    # 采用 Django-taggit 库
    tags = TaggableManager(blank=False, through=None)

    def __str__(self):
        return self.title

    # 浏览数，每一次浏览都自动加一
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_tags(self):
        tags = []
        self.tags.all()
        tags.append(str(tags))
        return ','.join(tags)

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('front_end:article_detail', args=[self.nid])


class ArticleDetail(models.Model):
    """
    文章详情表

    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid", on_delete=models.CASCADE)


class ArticleLike(models.Model):
    """
    喜欢表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid", null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", to_field="nid", null=True, on_delete=models.CASCADE)
    like_ip = models.CharField(max_length=20, verbose_name="评论电脑的IP", null=True)

    class Meta:
        unique_together = (("article", "user"),)


class Comment(MPTTModel):
    """
    评论表
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='comments')
    # mptt树形结构
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # 记录二级评论回复给谁, str
    reply_to = models.ForeignKey(UserInfo, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')
    body = models.CharField(max_length=800)  # 评论内容
    created = models.DateTimeField(verbose_name='创建时间')

    class MPTTMeta:
        order_insertion_by = ["-created"]

    def __str__(self):
        return self.body



class ad_poster(models.Model):
    """
    广告
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, verbose_name="广告标题")
    ad_url = models.CharField(max_length=50, verbose_name="广告链接")
    ad_photo = models.FileField(upload_to="advertisement/", verbose_name="广告图片")
    is_show = models.IntegerField(default=1, verbose_name="是否在前台展示")
    is_rotation = models.IntegerField(default=1, verbose_name="是否在前台轮播展示")
    create_time = models.DateTimeField(verbose_name='创建时间')  # 创建时间


class Links(models.Model):
    """
    :友情链接
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, verbose_name="链接名")
    url = models.CharField(max_length=50, verbose_name="链接URL")
    create_time = models.DateTimeField(verbose_name='创建时间')  # 创建时间
    is_show = models.IntegerField(default=1, verbose_name="是否在前台展示")
