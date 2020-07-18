import datetime
import os
import re
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown
from django.contrib import messages
from django.db.models import Q,F
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from Blog import settings
from front_end import models
from django.contrib.auth.decorators import login_required
from PIL import Image
from taggit.models import Tag
from taggit.models import TaggedItem
# from utils.mypage import Page
from front_end.forms import ArticleForm
from notifications.signals import notify


@login_required
def index(request):
	return render(request, "back_end/index.html")


def welcome(request):
	user_list = models.UserInfo.objects.all()
	article_list = models.Article.objects.all()
	comment_list = models.Comment.objects.all()

	return render(request, "back_end/welcome.html", {
		"user_list": user_list,
		"article_list": article_list,
		"comment_list": comment_list,
	})


def article_list(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1, user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	# article_list = models.Article.objects.filter().order_by('-create_time')
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()

	article_list = models.Article.objects.all().order_by('-create_time')
	paginator = Paginator(article_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)

	return render(request, "back_end/all_article.html", {
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"page": page,
	})


def all_article(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1, user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	article_list = models.Article.objects.filter().order_by('-create_time')
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()
	paginator = Paginator(article_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, "back_end/all_article.html", {
		"article_list": article_list,
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"page": page,
	})


def user_article(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1, user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()
	user_article_list = models.Article.objects.filter(user_id=user_id).order_by('-create_time')
	paginator = Paginator(user_article_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, "back_end/user_article.html", {
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"user_article_list": user_article_list,
		"page": page,
	})


def user_article_release(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1, user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()
	user_article_list = models.Article.objects.filter(user_id=user_id, is_release=1).order_by('-create_time')
	paginator = Paginator(user_article_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, "back_end/user_article_release.html", {
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"user_article_list": user_article_list,
		"page": page,
	})


def user_article_draft(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1, user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()
	user_article_list = models.Article.objects.filter(user_id=user_id, is_draft=1).order_by('-create_time')
	paginator = Paginator(user_article_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, "back_end/user_article_draft.html", {
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"user_article_list": user_article_list,
		"page": page,
	})


def user_article_review(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1,user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
		user_article_list = models.Article.objects.filter(is_review=1).order_by('-create_time')
		paginator = Paginator(user_article_list, 10)  # 实例化Paginator, 每页显示10条数据
		page = request.GET.get('page')
		try:
			page = paginator.page(page)  # 传递当前页的实例对象到前端
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()
		user_article_list = models.Article.objects.filter(user_id=user_id, is_review=1).order_by('-create_time')
		paginator = Paginator(user_article_list, 10)  # 实例化Paginator, 每页显示10条数据
		page = request.GET.get('page')
		try:
			page = paginator.page(page)  # 传递当前页的实例对象到前端
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)
	return render(request, "back_end/user_article_review.html", {
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"user_article_list": user_article_list,
		"page": page,
	})


def user_article_recycle(request):
	user_id = request.user.pk
	article_user_count = models.Article.objects.filter(user_id=user_id).count()
	article_draft_count = models.Article.objects.filter(is_draft=1, user_id=user_id).count()
	article_release_count = models.Article.objects.filter(is_release=1, user_id=user_id).count()
	article_recycle_count = models.Article.objects.filter(is_recycle=1, user_id=user_id).count()
	article_count = models.Article.objects.count()
	if request.user.is_superuser:
		article_review_count = models.Article.objects.filter(is_review=1).count()
	else:
		article_review_count = models.Article.objects.filter(is_review=1, user_id=user_id).count()
	user_article_list = models.Article.objects.filter(user_id=user_id, is_recycle=1).order_by('-create_time')
	paginator = Paginator(user_article_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, "back_end/user_article_recycle.html", {
		"article_count": article_count,
		"article_user_count": article_user_count,
		"article_draft_count": article_draft_count,
		"article_review_count": article_review_count,
		"article_release_count": article_release_count,
		"article_recycle_count": article_recycle_count,
		"user_article_list": user_article_list,
		"page": page,
	})


def article_class(request):
	class_list = models.Classification.objects.all()
	return render(request, "back_end/class_list.html", {
		"class_list": class_list,
	})


def article_class_edit(request, class_pk):
	if request.method == "POST":
		ret = {"status": 0}
		new_title = request.POST.get("title")
		updata_class = models.Classification.objects.get(nid=class_pk)
		class_title = models.Classification.objects.all().values('title')
		all_class = []
		for a_class in class_title:
			all_class.append(a_class['title'])
		if updata_class.title == new_title:
			return JsonResponse(ret)
		else:
			if new_title.lower() in [all_c.lower() for all_c in all_class ]:
				return JsonResponse(ret)
			else:
				ret = {"status": 1}
				updata_class.title = new_title
				updata_class.save()
				return JsonResponse(ret)

	article_class = models.Classification.objects.get(nid=class_pk)
	return render(request, "back_end/class_edit.html", {
		"article_class": article_class,
	})


def article_class_delete(request):
	if request.method == "POST":
		class_pk = request.POST.get("pid")
		delete_class = models.Classification.objects.get(nid=class_pk)
		delete_class.delete()
	return HttpResponse('成功！')


def article_class_add(request):
	global title
	if request.method == "POST":
		new_title = request.POST.get('title')
		title = models.Classification.objects.values_list('title', flat=True).all()
		if new_title in title:
			ret = {"status": 0}
			return JsonResponse(ret)
		models.Classification.objects.create(title=new_title)
		ret = {"status": 1}
		return JsonResponse(ret)
	return render(request, 'back_end/class_list.html')


#   添加文章
def article_add(request):
	if request.method == "POST":
		article_form = ArticleForm(request.POST, request.FILES)
		article_content = request.POST.get('article_content')
		desc = article_content[0:130] + "..."
		cover_photo = request.FILES.get("avatar")
		user = request.user
		now = datetime.datetime.now()
		article_class = request.POST.get('class')
		if article_form.is_valid():
			# 保存数据，但暂时不提交到数据库中
			new_article = article_form.save(commit=False)
			# 指定登录的用户为作者
			new_article.user = user
			class_id = models.Classification.objects.get(title=article_class)
			new_article.classification = class_id
			new_article.desc = desc
			new_article.create_time = now

			if cover_photo == None or cover_photo == '':
				new_article.save()
			else:
				cover_photo = "cover_photo/" + str(cover_photo)
				local_file = settings.MEDIA_ROOT + '/' + cover_photo
				data = request.FILES['avatar']
				with open(local_file, 'wb+') as f:
					for chunk in data.chunks():
						f.write(chunk)
				new_article.cover_photo = cover_photo
				new_article.save()

			# 保存 tags 的多对多关系
			article_form.save_m2m()
			# 完成后返回到文章列表

			models.ArticleDetail.objects.create(content=article_content, article=new_article)
			ret = {"status": 1, "msg": "保存到草稿箱，成功！"}
			return JsonResponse(ret)
	class_list = models.Classification.objects.all()
	tags = Tag.objects.all()
	return render(request, "back_end/article_add.html", {
		"class_list": class_list,
		"tags": tags,
	})



# 添加文章，并直接提交审核
def article_add_review(request):
	if request.method == "POST":
		article_form = ArticleForm(request.POST, request.FILES)
		article_content = request.POST.get('article_content')
		desc = article_content[0:130] + "..."
		cover_photo = request.FILES.get("avatar")
		user = request.user
		now = datetime.datetime.now()
		article_class = request.POST.get('class')
		if article_form.is_valid():
			# 保存数据，但暂时不提交到数据库中
			new_article = article_form.save(commit=False)
			# 指定登录的用户为作者
			new_article.user = user
			class_id = models.Classification.objects.get(title=article_class)
			new_article.classification = class_id
			new_article.desc = desc
			new_article.create_time = now
			new_article.is_draft = 0
			new_article.is_review = 1

			if cover_photo == None or cover_photo == '':
				new_article.save()
			else:
				cover_photo = "cover_photo/" + str(cover_photo)
				local_file = settings.MEDIA_ROOT + '/' + cover_photo
				data = request.FILES['avatar']
				with open(local_file, 'wb+') as f:
					for chunk in data.chunks():
						f.write(chunk)
				new_article.cover_photo = cover_photo
				new_article.save()

			# 保存 tags 的多对多关系
			article_form.save_m2m()
			# 完成后返回到文章列表

			models.ArticleDetail.objects.create(content=article_content, article=new_article)
			# 给管理员发送审核通知
			spuer_users = models.UserInfo.objects.filter(is_superuser=1).all()
			for spuer_user in spuer_users:
				notify.send(
					spuer_user,
					recipient=user,
					verb='文章已经提交审核，请尽快审核！',
					target=new_article,
					action_object=new_article,
				)

			ret = {"status": 1, "msg": "提交审核，成功！"}
			return JsonResponse(ret)
	class_list = models.Classification.objects.all()
	tags = Tag.objects.all()
	return render(request, "back_end/article_add.html", {
		"class_list": class_list,
		"tags": tags,
	})


#   修改文章
def article_updata_details(request, article_pk):
	if request.method == "POST":
		new_title = request.POST.get('title')
		new_article_content = request.POST.get('article_content')
		new_article_class = request.POST.get('class')
		new_cover_photo = request.FILES.get("cover_photo")
		new_desc = new_article_content[0:150] + "..."
		new_create_time = datetime.datetime.now()
		new_tags = request.POST.get('tags').split(',')
		new_class_id = models.Classification.objects.values('nid').get(title=new_article_class)
		new_class_id = new_class_id["nid"]
		if new_cover_photo == None or new_cover_photo == '':
			models.Article.objects.filter(nid=article_pk).update(title=new_title, desc=new_desc,
																 create_time=new_create_time,
																 classification=new_class_id)
			models.ArticleDetail.objects.filter(article=article_pk).update(content=new_article_content)
		else:
			cover_photo = "cover_photo/" + str(new_cover_photo)
			local_file = settings.MEDIA_ROOT + '/' + cover_photo
			data = request.FILES['avatar']
			with open(local_file, 'wb+') as f:
				for chunk in data.chunks():
					f.write(chunk)
			models.Article.objects.filter(nid=article_pk).update(title=new_title, desc=new_desc,
																 cover_photo=new_cover_photo,
																 create_time=new_create_time,
																 classification=new_class_id)
			models.ArticleDetail.objects.filter(article=article_pk).update(content=new_article_content)

		article_obj = models.Article.objects.get(nid=article_pk)
		# article_obj.tags.set(new_tags,clear=True)
		# 直接提交的tags里有空格,所以要把空格去除，否则带空格的又是一个新的tag
		tag_list = []
		for tag in new_tags:
			tag = ''.join(tag.split())
			tag_list.append(tag)
		article_obj.tags.set(*tag_list,clear=True)
		# 完成后返回到文章列表
		ret = {"status": 1, "msg": "修改文章，成功！"}
		return JsonResponse(ret)
	article = models.Article.objects.get(nid=article_pk)
	class_list = models.Classification.objects.all()
	article_details = models.ArticleDetail.objects.filter(article=article_pk).first()
	article_tags = u"," .join(o.name for o in article.tags.all())
	tags = Tag.objects.all()
	return render(request, "back_end/article_updata_datails.html", {
		"article": article,
		"details": article_details,
		"class_list": class_list,
		"article_tags": article_tags,
		"tags": tags,
	})


def comment_list(request):
	user = request.user
	user_super = user.is_superuser
	if user_super == True:
		comment = models.Comment.objects.all().order_by("-created")
	else:
		comment = models.Comment.objects.filter(Q(user=user)|Q(reply_to=user)).order_by("-created")
	paginator = Paginator(comment, 25)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, "back_end/comment_list.html", {
		"page": page,
	})


def comment_update(request,pk):
	if request.method == "POST":
		title= request.POST.get("title")
		models.Comment.objects.filter(id=pk).update(body=title)
		ret = {"status": 1, "msg": "修改成功！"}
		return JsonResponse(ret)
	comment = models.Comment.objects.filter(id=pk)
	return render(request,"back_end/comment_update.html",{
		"comments": comment,
	})

def comment_del(request):
	if request.method == "POST":
		nid = request.POST.get("pid")
		comments = models.Comment.objects.filter(id=nid)

		for comment in comments:
			comment_num = comment.get_descendant_count() # 计算出当期节点下的所有子节点个数。不包括所在节点
			comment_num = comment_num + 1
			models.Article.objects.filter(nid=comment.article_id).update(comment_count=F("comment_count") - comment_num)
			models.Comment.objects.filter(id=nid).delete()
			old_comment = models.Article.objects.get(nid=comment.article_id)
			if old_comment.comment_count < 0:
				old_comment.comment_count = 0
				old_comment.save()
			ret = {"status": 1, "msg": "删除成功！"}
			return JsonResponse(ret)


def comment_all_del(request):
	if request.method == "POST":
		nids = request.POST.get('pid')
		nids_list = nids.split(',')
		for nid in nids_list:
			comments = models.Comment.objects.filter(id=nid)
			for comment in comments:
				models.Article.objects.filter(nid=comment.article_id).update(comment_count=F("comment_count") - 1)
				models.Comment.objects.filter(id=nid).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)
	ret = {"status": 0, "msg": "删除失败！"}
	return JsonResponse(ret)



# 博客文章插入图片
@csrf_exempt
def api_upload_url(request):
	if request.method == "POST":
		data = request.FILES['editormd-image-file']
		img = Image.open(data)
		width = img.width
		height = img.height
		rate = 1.0  # 压缩率
		# 根据图像大小设置压缩率
		if width >= 2000 or height >= 2000:
			rate = 0.3
		elif width >= 1000 or height >= 1000:
			rate = 0.5
		elif width >= 500 or height >= 500:
			rate = 0.8
		width = int(width * rate)  # 新的宽
		height = int(height * rate)  # 新的高
		img.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图
		# 本地创建保存图片的文件夹
		path = settings.STATIC_URL + 'upload/' + time.strftime('%Y%m%d') + '/'
		if not os.path.exists(settings.BASE_DIR + path):
			os.makedirs(settings.BASE_DIR + path)
		# 拼装本地保存图片的完整文件名
		filename = time.strftime('%H%M%S') + '_' + data.name
		local_file = settings.BASE_DIR + path + filename

		# 写入文件
		with open(local_file, 'wb+') as f:
			for chunk in data.chunks():
				f.write(chunk)
		try:
			img.save(local_file)
			url = '/static' + local_file.split('static')[-1]
			return JsonResponse({'success': 1, 'message': '成功', 'url': url})
		except Exception as e:
			return JsonResponse({'success': 0, 'message': '上传失败'})


#   查看文章(markdown格式文件)
def article_view(request, pk):
	article_details = models.ArticleDetail.objects.filter(article=pk).first()
	article_details.content = markdown.markdown(article_details.content.replace("\r\n", '  \n'), extensions=[
		'markdown.extensions.extra',
		'markdown.extensions.codehilite',
		'markdown.extensions.toc',
	], safe_mode=True, enable_attributes=False)
	return render(request, "back_end/article_view.html", {
		"details": article_details,
	})


def draft_recycle(request):
	if request.method == 'POST':
		article_id = request.POST.get('pid')
		edit_draft = models.Article.objects.get(pk=article_id)
		edit_draft.is_draft = 0
		edit_draft.is_recycle = 1
		edit_draft.save()
	return render(request, "back_end/user_article_draft.html")


def draft_review(request):
	if request.method == 'POST':
		article_id = request.POST.get('pid')
		edit_draft = models.Article.objects.get(pk=article_id)
		edit_draft.is_draft = 0
		edit_draft.is_review = 1
		edit_draft.save()
		# 给管理员发送审核通知
		users= models.UserInfo.objects.filter(is_superuser=1).all()
		for user in users:
			notify.send(
				edit_draft.user,
				recipient=user,
				verb='文章已经提交审核，请尽快审核！',
				target=edit_draft,
				action_object=edit_draft,
			)
	return render(request, "back_end/user_article_draft.html")


def recycle_draft(request):
	if request.method == 'POST':
		article_id = request.POST.get('pid')
		edit_recycle = models.Article.objects.get(pk=article_id)
		edit_recycle.is_draft = 1
		edit_recycle.is_recycle = 0
		edit_recycle.create_time = datetime.datetime.now()
		edit_recycle.save()
	return render(request, "back_end/user_article_recycle.html")


def recycle_delete(request):
	if request.method == "POST":
		article_pk = request.POST.get("pid")
		delete_recycle = models.Article.objects.get(pk=article_pk)
		delete_recycle.delete()
	return render(request, "back_end/user_article_recycle.html")

def review_view(request, article_pk):
	article_details = models.ArticleDetail.objects.filter(article=article_pk).first()
	return render(request, "back_end/review_view.html", {
		"article": article_details,
	})


def review_yes(request):
	if request.method == "POST":
		article_pk = request.POST.get("pid")
		edit_review = models.Article.objects.get(pk=article_pk)
		edit_review.is_release = 1
		edit_review.is_review = 0
		edit_review.create_time = datetime.datetime.now()
		edit_review.save()
		# 给用户发送通知
		notify.send(
			request.user,
			recipient=edit_review.user,
			verb='你的文章审核通过，已发布！',
			target=edit_review,
			action_object=edit_review,
		)
	return render(request, "back_end/user_article_review.html")


def review_no(request):
	if request.method == "POST":
		article_pk = request.POST.get("pid")
		edit_review = models.Article.objects.get(pk=article_pk)
		edit_review.is_draft = 1
		edit_review.is_review = 0
		edit_review.create_time = datetime.datetime.now()
		edit_review.save()
		# 给用户发送通知
		notify.send(
			request.user,
			recipient=edit_review.user,
			verb='你的文章审核没有通过，已返回你的草稿箱，请修改！',
			target=edit_review,
			action_object=edit_review,
		)
	return render(request, "back_end/user_article_review.html")


def admin_index(request):
	user = request.user
	my_details = models.UserInfo.objects.get(nid=user.pk)
	return render(request, 'back_end/admin_index.html', {
		"my_details": my_details,
	})


def admin_list(request):
	user_list = models.UserInfo.objects.all()
	paginator = Paginator(user_list, 10)  # 实例化Paginator, 每页显示10条数据
	page = request.GET.get('page')
	try:
		page = paginator.page(page)  # 传递当前页的实例对象到前端
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, 'back_end/admin_list.html', {
		"page": page,
	})


def admin_updata_details(request):
	if request.method == "POST":
		ret = {"status": 0, "msg": ""}
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		avatar = request.FILES.get("avatar")
		# print(models.UserInfo.objects.filter(~Q(pk=request.user.pk)).values_list('username',flat=True)) ## 用~Q查询来查找不是id以外的数据
		if username == None or username == "":
			ret = {"status": 0, "msg": "用户名不能为空！"}
			return JsonResponse(ret)
		else:
			is_user = models.UserInfo.objects.filter(~Q(pk=request.user.pk)).values_list('username', flat=True)
			if username in is_user:
				ret = {"status": 0, "msg": "用户名已存在，请重新输入！"}
				return JsonResponse(ret)
			else:
				if password == None or password == "":
					ret = {"status": 0, "msg": "密码不能为空，请输入！"}
					return JsonResponse(ret)
				else:
					if len(password) < 6:
						ret = {"status": 0, "msg": "密码不能小于6位，请重新输入！"}
						return JsonResponse(ret)
					else:
						password = make_password(password)
						if email == None or email == "":
							ret = {"status": 0, "msg": "邮箱不能为空，请输入！"}
							return JsonResponse(ret)
						else:
							is_email1 = re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email)
							if is_email1:
								is_email2 = models.UserInfo.objects.filter(~Q(pk=request.user.pk)).values_list('email',
																											   flat=True)
								if email in is_email2:
									ret = {"status": 0, "msg": "该邮箱已经存在，请重新输入！"}
									return JsonResponse(ret)
								else:
									if phone == None or phone == "":
										ret = {"status": 0, "msg": "手机号不能为空，请输入！"}
										return JsonResponse(ret)
									else:
										is_phone = re.match(r"^1[35678]\d{9}$", phone)
										if is_phone:
											is_phone2 = models.UserInfo.objects.filter(
												~Q(pk=request.user.pk)).values_list('phone', flat=True)
											if phone in is_phone2:
												ret = {"status": 0, "msg": "该手机号已经存在，请重新输入！"}
												return JsonResponse(ret)
											else:
												if avatar == None or avatar == '':
													models.UserInfo.objects.filter(pk=request.user.pk).update(
														username=username,
														password=password, email=email, phone=phone)
													ret = {"status": 1, "msg": "修改信息成功！"}
													return JsonResponse(ret)
												else:

													avatar = "avatars/" + str(avatar)
													local_file = settings.MEDIA_ROOT + '/' + avatar
													data = request.FILES['avatar']
													with open(local_file, 'wb+') as f:
														for chunk in data.chunks():
															f.write(chunk)
													models.UserInfo.objects.filter(pk=request.user.pk).update(
														username=username,
														password=password,
														email=email,
														phone=phone, avatar=avatar)
													ret = {"status": 1, "msg": "修改信息成功！"}
													return JsonResponse(ret)
										else:
											ret = {"status": 0, "msg": "手机号格式错误，请重新输入！"}
											return JsonResponse(ret)
							else:
								ret = {"status": 0, "msg": "邮箱格式错误，请重新输入！"}
								return JsonResponse(ret)

	user = request.user
	my_details = models.UserInfo.objects.get(nid=user.pk)
	return render(request, 'back_end/admin_updata_details.html', {
		"my_details": my_details,
	})


def admin_ad_poster(request):
	ad_poster = models.ad_poster.objects.all()
	return render(request, 'back_end/ad_poster.html', {
		"ad_poster": ad_poster,
	})


def ad_poster_add(request):
	if request.method == "POST":
		title = request.POST.get('title')
		url = request.POST.get('url')
		ad_photo = request.FILES.get("avatar")
		if title == None or title == "":
			ret = {"status": 0, "msg": "广告标题不能为空！"}
			return JsonResponse(ret)
		else:
			if url == None or url == "":
				ret = {"status": 0, "msg": "广告链接不能为空！"}
				return JsonResponse(ret)
			else:
				if ad_photo == None or ad_photo == "":
					ret = {"status": 0, "msg": "广告图片不能为空！"}
					return JsonResponse(ret)
				else:
					ad_photo = "advertisement/" + str(ad_photo)
					local_file = settings.MEDIA_ROOT + '/' + ad_photo
					data = request.FILES['avatar']
					with open(local_file, 'wb+') as f:
						for chunk in data.chunks():
							f.write(chunk)
					models.ad_poster.objects.create(title=title, ad_url=url, ad_photo=ad_photo,
													create_time=datetime.datetime.now())
					ret = {"status": 1, "msg": "添加广告成功！"}
					return JsonResponse(ret)
	return render(request, 'back_end/ad_poster_add.html')


def ad_poster_del(request):
	if request.method == "POST":
		nid = request.POST.get("pid")
		models.ad_poster.objects.filter(pk=nid).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)


def ad_poster_all_del(request):
	if request.method == "POST":
		nids = request.POST.get('pid')
		nids_list = nids.split(',')
		models.ad_poster.objects.filter(nid__in=nids_list).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)
	ret = {"status": 0, "msg": "删除失败！"}
	return JsonResponse(ret)


def ad_poster_is_show(request):
	if request.method == "POST":
		nid = request.POST.get('pid')
		is_show = request.POST.get('is_show')
		if int(is_show) == 1:
			models.ad_poster.objects.filter(pk=nid).update(is_show=0)
			ret = {"status": 1}
			return JsonResponse(ret)
		else:
			models.ad_poster.objects.filter(pk=nid).update(is_show=1)
			ret = {"status": 1}
			return JsonResponse(ret)


def ad_poster_update(request, ad_pk):
	if request.method == "POST":
		title = request.POST.get('title')
		ad_url = request.POST.get('url')
		is_show = request.POST.get('is_show')
		is_rotation = request.POST.get('is_rotation')
		ad_photo = request.FILES.get("avatar")
		if title == None or title == "":
			ret = {"status": 0, "msg": "标题不能为空，请输入标题！"}
			return JsonResponse(ret)
		else:
			if ad_url == None or ad_url == " ":
				ret = {"status": 0, "msg": "链接不能为空，请输入链接！"}
				return JsonResponse(ret)
			else:
				if ad_photo == None or ad_photo == "":
					models.ad_poster.objects.filter(nid=ad_pk).update(title=title, ad_url=ad_url, is_show=int(is_show),
																	  is_rotation=int(is_rotation),
																	  create_time=datetime.datetime.now())
					ret = {"status": 1, "msg": "修改成功！"}
					return JsonResponse(ret)
				else:
					ad_photo = "advertisement/" + str(ad_photo)
					local_file = settings.MEDIA_ROOT + '/' + ad_photo
					data = request.FILES['avatar']
					with open(local_file, 'wb+') as f:
						for chunk in data.chunks():
							f.write(chunk)
					models.ad_poster.objects.filter(nid=ad_pk).update(title=title, ad_url=ad_url, is_show=int(is_show),
																	  is_rotation=int(is_rotation), ad_photo=ad_photo,
																	  create_time=datetime.datetime.now())
					ret = {"status": 1, "msg": "修改成功！"}
					return JsonResponse(ret)
	ad_poster = models.ad_poster.objects.get(nid=ad_pk)
	return render(request, 'back_end/ad_poster_update.html', {
		"ad_poster": ad_poster,
	})


def links(request):
	links = models.Links.objects.all()
	return render(request, 'back_end/links.html', {
		"links": links,
	})


def links_add(request):
	if request.method == "POST":
		title = request.POST.get("title")
		url = request.POST.get("url")
		models.Links.objects.create(title=title,url=url,create_time=datetime.datetime.now())
		ret = {"status": 1, "msg": "添加友情链接成功！"}
		return JsonResponse(ret)

	return render(request,"back_end/links_add.html")


def links_update(request,pk):
	if request.method == "POST":
		print(request.POST)
		title = request.POST.get('title')
		url = request.POST.get('url')
		is_show = request.POST.get('is_show')
		models.Links.objects.filter(nid=pk).update(title=title,url=url,is_show=int(is_show),create_time=datetime.datetime.now())
		ret = {"status": 1, "msg": "修改成功！"}
		return JsonResponse(ret)
	links = models.Links.objects.get(nid=pk)
	return render(request,"back_end/links_update.html",{
		"links": links,
	})


def links_is_show(request):
	if request.method == "POST":
		nid = request.POST.get('pid')
		is_show = request.POST.get('is_show')
		if int(is_show) == 1:
			models.Links.objects.filter(pk=nid).update(is_show=0)
			ret = {"status": 1}
			return JsonResponse(ret)
		else:
			models.Links.objects.filter(pk=nid).update(is_show=1)
			ret = {"status": 1}
			return JsonResponse(ret)


def links_del(request):
	if request.method == "POST":
		nid = request.POST.get("pid")
		models.Links.objects.filter(pk=nid).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)


def links_all_del(request):
	if request.method == "POST":
		nids = request.POST.get('pid')
		nids_list = nids.split(',')
		models.Links.objects.filter(nid__in=nids_list).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)
	ret = {"status": 0, "msg": "删除失败！"}
	return JsonResponse(ret)


def user_is_superuser(request):
	if request.method == "POST":
		nid = request.POST.get('pid')
		is_superuser = request.POST.get('is_superuser')
		if int(is_superuser) == 1:
			models.UserInfo.objects.filter(pk=nid).update(is_superuser=0)
			ret = {"status": 1}
			return JsonResponse(ret)
		else:
			models.UserInfo.objects.filter(pk=nid).update(is_superuser=1)
			ret = {"status": 1}
			return JsonResponse(ret)


def user_del(request):
	if request.method == "POST":
		nid = request.POST.get("pid")
		models.UserInfo.objects.filter(pk=nid).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)


def user_all_del(request):
	if request.method == "POST":
		nids = request.POST.get('pid')
		nids_list = nids.split(',')
		models.UserInfo.objects.filter(nid__in=nids_list).delete()
		ret = {"status": 1, "msg": "删除成功！"}
		return JsonResponse(ret)
	ret = {"status": 0, "msg": "删除失败！"}
	return JsonResponse(ret)


# 下架文章
def release_draft(request):
	if request.method == 'POST':
		article_id = request.POST.get('pid')
		article = models.Article.objects.get(pk=article_id)
		article.is_release = 0
		article.is_draft = 1
		article.create_time = datetime.datetime.now()
		article.save()
	return render(request,'back_end/user_article_release.html')
