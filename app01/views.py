from django.shortcuts import render, redirect, HttpResponse
from rbac import models as rbac_models
from rbac.service.init_permission import init_permission
import re


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
            print(user_obj)

            init_permission(request, user_obj)
            return redirect('/index/')


def index(request):
    return render(request, 'index.html')


def test(request):

    return render(request, 'test.html')
