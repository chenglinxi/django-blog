from django.contrib import admin
from front_end import models

# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Classification)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.Label)
admin.site.register(models.ArticleLike)
admin.site.register(models.EmailVerifyRecord)