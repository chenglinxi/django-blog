# blog
基于django的个人博客

## 环境：
基于`python3.8`和`Django3.0`的博客。   

## 主要功能：
- 文章，页面，分类目录，标签的添加，删除，编辑等。文章及页面支持`Markdown`，支持代码高亮。
- 支持文章全文搜索。
- 完整的评论功能，包括发表回复评论，支持多级评论。
- 侧边栏功能，最新文章，最多阅读，标签云等。
- 网站异常邮件提醒，若有未捕捉到的异常会自动发送提醒邮件。

## templates目录树
.
├── back_end    # 后端页面
│   ├── ad_poster.html      #广告管理页面
│   ├── ad_poster_add.html      #广告增加页面
│   ├── ad_poster_update.html       #广告更新页面
│   ├── admin_index.html     #个人用户管理页面
│   ├── admin_list.html     #全体用户管理页面
│   ├── admin_updata_details.html     #个人用户更新页面
│   ├── all_article.html     #所有文章页面
│   ├── article_add.html     #文章增加页面
│   ├── article_list.html     #个人所有文章页面
│   ├── article_updata_datails.html     #个人文章修改页面
│   ├── article_view.html     #文章预览页面
│   ├── class_edit.html      #文章类别修改页面
│   ├── class_list.html      #文章类别管理页面
│   ├── comment_list.html   #评论管理页面
│   ├── comment_update.html     #评论更新页面
│   ├── error.html       #错误页面
│   ├── index.html      #后台主页面
│   ├── links.html      #友情链接管理页面
│   ├── links_add.html      #友情链接增加页面
│   ├── links_update.html      #友情链接修改页面
│   ├── master.html     #后台模板页面
│   ├── page.html    #分页脚本页面
│   ├── review_view.html      #审核详情页面
│   ├── user_article.html   #个人文章页面
│   ├── user_article_draft.html   #草稿箱页面
│   ├── user_article_recycle.html    #回收站页面
│   ├── user_article_release.html   #发布页面
│   ├── user_article_review.html    #审核页面
│   └── welcome.html      #后台欢迎页面   
├── front_end    #前端页面
│   ├── article_category.html   #按类别文章页面
│   ├── article_class.html       #类别模块
│   ├── article_data.html   #按日期归纳文章页面
│   ├── article_details.html  #文章详情页面
│   ├── article_tags.html #按标签文章页面
│   ├── author_article.html #按作者文章页面   
│   ├── author_leaving.html #留言页面
│   ├── confirm.html    # 邮箱激活确认页面
│   ├── data_menu.html    #日期归纳模块
│   ├── forgot_password.html    #忘记密码页面
│   ├── home.html   #主页面
│   ├── home_page.html  #分页模块
│   ├── like.html  #最喜欢模块
│   ├── links.html  #友情链接模块
│   ├── login.html    #登录页面
│   ├── master.html     #前端模板
│   ├── register.html   #用户注册页面
│   ├── results.html    # 搜索信息页面
│   ├── tags.html       #云标签模块
│   ├── master.html     #文章标签模块
│   ├── update_password.html    #忘记密码重设页面
│   └── weixin.html 
├── notice
│   └── list.html



