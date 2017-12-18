### 权限管理

*我们可以根据角色的不同而分配不同的功能给角色，也就是分配给角色不同的url来处理不同的功能，而对于一个项目来说，分配权限应该单独设定一项功能app，以便不和其他功能型软件冲突以及后续的扩展*

### 设计思路

1. 创建app，将有关权限的内容都放在这个app里面
2. 设计表结构，分别为角色，权限，菜单，用户等等，让不同的角色对应不同的url，设计对应的关系
3. 创建用户登录，一旦用户登录成功，就会从数据库获取用户对应的权限，并保存在session中，避免每次用户登录都从数据库中提取数据
4. 设置超时时间，每隔一段时间让session更新一次，防止数据库中数据改变导致不能和session保持一致

### RBAC(基于角色的权限控制)role basic access control

表关系设置:

有三个表，分别为用户、角色、权限、菜单

角色——多对多——权限

用户——多对多——角色

权限表：

*显示权限的URL*

| ID   | 标题   | URL（正则表达式） | 菜单ID（Null） |
| ---- | ---- | ---------- | ---------- |
|      |      |            |            |

角色表

*用户是不断变化的，如果更换用户的话，权限又要重新设置*

| ID   | 标题   |
| ---- | ---- |
|      |      |

角色—多对多—权限

*表示角色和权限多对多的关系*

| ID   | 角色ID | 权限ID |
| ---- | ---- | ---- |
|      |      |      |

用户表

*表示用户*

| ID   | 姓名   | 性别   | 用户名  | 密码   |
| ---- | ---- | ---- | ---- | ---- |
|      |      |      |      |      |

用户—多对多—角色

*表示用户和角色多对多的关系*

| ID   | 用户ID | 角色ID |
| ---- | ---- | ---- |
|      |      |      |

菜单表

*有可能权限太多，因此需要对权限分类，而且，如果权限太复杂的话，需要多级分类*

| ID   | 标题   | 父级菜单ID |
| ---- | ---- | ------ |
|      |      |        |

### 创建权限管理

* 创建名为rbac的app，在model文件下创建表关系


* 在setting文件中配置rbac应用


* 在主程序中写用户登录配置，包括url，view，
* 在view中，根据用户登录的信息提取用户中的权限，获取菜单


* 将权限写入到session中去（以后再次请求时，取session中检查即可）

### 检查用户发送的请求的URL去当前用户的session中匹配

中间件实现

* process_request(self, request)
* 获取request.path_info当前用户发送的URL
* 获取request.session[权限]获取当前用户所有的权限
* 匹配当前用户发送的URL在不在当前用户所有的URL里面，如果成功，无，如果失败的话，返回数据
* 登录页面无需任何权限就可以访问

### 拿到数据后自动生成权限菜单

* session中取菜单相关：包括所有的菜单和可以在菜单上显示的URL
* 取得数据后通过循环等实现多级菜单的效果

### 前段显示权限菜单

通过自定义标签的方式，在前端生成多级菜单，需要用到递归等方法

需要怎样样式的话，可以提前写好样式，然后以静态文件的方式导入

### 对权限表进行增删改查

使用model_form进行对表的增删改查

在模板进行循环显示

### 框架使用方法

配置应用

````python
INSTALLED_APPS = [
    'app01',
    'rbac',
]
````

向数据库中添加表，首先删除migration里面的数据，然后执行一下语句

```python
python3 manage.py makemigrations
python3 manage.py migrate
```

这样就可以使用了，模板用的是主应用里面的模板



配置中间件

````python
MIDDLEWARE = [
    'rbac.middleware.rbac.RbacMiddleware',
]
````

配置session的key，登录路径以及不用权限就可以访问的URL

```python
# ##################################### rbac 权限相关配置 

# 保存用户权限的Session Key
SESSION_PERMISSION_URL_KEY = "afikjmdlalemnasldkfaeasfd"

SESSION_PERMISSION_MENU_URL_KEY = "sdfasd3234xdfsdf23sdfsdf"
ALL_MENU_KEY = "k1"
PERMISSION_URL_KEY = "k2"

LOGIN_URL = "/login.html"  # 登录页面URL

URL_REGEX = "^{0}$"    # 用于格式化路径

PASS_URL_LIST = [     # 配置不用权限就可以访问的URL
    "/login.html",
    "/test.html",
    '/admin/.*',
    '/rbac/.*'
]
```

配置路由，使路由转接到rbac的路由系统上面

```python
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rbac/', include('rbac.urls')),  # 添加权限路由分发
    url(r'^login.html/', views.login),
    url(r'^test.html/', views.test),
    url(r'^index.html/', views.index),
]
```



在用户登录的view中配置导入rbac中的model和init_permission以及执行init_permission函数

```python
from django.shortcuts import render,HttpResponse,redirect
from rbac import models as rbac_models
from rbac.service.init_permission import init_permission

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        user_obj = rbac_models.UserInfo.objects.filter(username=user, password=pwd).first()
        if not user_obj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            # 获取当前用户所有权限
            # 获取菜单
            # 写入session
            init_permission(request,user_obj)
            return redirect('/index.html')
```

