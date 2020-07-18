from django import template
from front_end import models
from django.db.models import Count
from taggit.models import Tag
from taggit.models import TaggedItem

register = template.Library()


@register.inclusion_tag("front_end/article_class.html")
def get_article_class():
    title = models.Classification.objects.all()
    return {"title_all":title}


@register.inclusion_tag("front_end/data_menu.html")
def get_data_menu():
    # 按日期归档
    archive_list = models.Article.objects.filter(is_release=1).all().extra(
        select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).order_by("-archive_ym").values("archive_ym", "c")

    # 另外一种方法
    # article_list = models.Article.objects.all()
    # archive_list = []
    #
    # for article in article_list:
    #     # 将每一个文章的发布日期都获取出来，按照'%Y/%m'进行格式化
    #     pub_date = article.create_time.strftime('%Y/%m')
    #     if pub_date not in archive_list:
    #         # 如果这个时间字符串不在article_list这个列表中，就把这个年月添加进去
    #         archive_list.append(pub_date)
    return {
        "archive_list": archive_list,
    }

@register.inclusion_tag("front_end/tags.html")
def get_tags_list():
    tags = Tag.objects.all()
    tags_list = []
    for tag in tags:

        tag_name = tag.name
        # tag_num = TaggedItem.objects.filter(tag__name=tag).count()  #这里求每一个tag的数量(包括草稿箱里的，要的是已经发布的数量)
        is_release = models.Article.objects.filter(tags__name__in=[tag_name])
        is_release_num = is_release.filter(is_release=1).all().count() #这里得到每一个tag的数量已经发布的数量)
        # 剔除没有发布的文章（还在草稿箱或在审核中的文章）
        if is_release_num != 0:
            tag_dict = {"tag_name":tag_name,"tag_num": is_release_num}
            tags_list.append(tag_dict)
    return{
        "tags_list": tags_list,
    }


@register.inclusion_tag("front_end/ad_poster.html")
def get_ad_list():
    ad_list = models.ad_poster.objects.filter(is_show=1).order_by('-create_time')[0:5]
    return {
        "ad_list": ad_list,
    }

@register.inclusion_tag("front_end/links.html")
def get_links():
    links = models.Links.objects.filter(is_show=1).all()
    
    return{
        "links": links,
    }

@register.inclusion_tag("front_end/like.html")
def get_likes():
    likes= models.Article.objects.filter(is_release=1).order_by("-comment_count")[0:10]
    return{
        "likes":likes,
    }