"""
blog用到的form类
"""

from django import forms
from django.core.exceptions import ValidationError
from front_end import models
from mptt.models import MPTTModel


class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label='用户名',
        error_messages={
            "required": "用户名不能为空！",
            "max_length": "用户名最长不能超过16位",
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control",
            },
        )
    )
    password = forms.CharField(
        min_length=6,
        label='密码',
        error_messages={
            "required": "密码不能为空！",
            "min_length": "密码最短不能少于6位",
        },
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        )
    )
    re_password = forms.CharField(
        label='确认密码',
        error_messages={
            "required": "确认密码不能为空！",
        },
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        )
    )
    email = forms.EmailField(
        label="常用邮件地址",
        widget=forms.widgets.EmailInput(
            attrs={"class": "form-control"},

        ),
        error_messages={
            "invalid": "邮箱格式不正确！",
            "required": "邮箱不能为空!",
        }
    )

    # 重写username的局部钩子，对用户名是否存在做校验
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error("username", ValidationError("用户名已存在！"))
        else:
            return username

    # 重写email的局部钩子，对用户名是否存在做校验
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            self.add_error("email", ValidationError("邮箱已存在！"))
        else:
            return email

    # 重写全局的钩子函数，对确认密码做校验
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("两次密码不一致！"))
        else:
            return self.cleaned_data


# 写文章的表单类
class ArticleForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = models.Article
        # 定义表单包含的字段
        fields = ('title', 'tags', 'cover_photo')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
