from django.shortcuts import render, redirect
from . import models
# Create your views here.


def users(request):
    user_list = models.UserInfo.objects.all()
    return render(request, 'rbac/users.html', {'user_list': user_list})

from django.forms import ModelForm
from django.forms import widgets as wid


# 创建ModelForm类
class UserModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        # fields = ['username', 'nickname'],可以只显示列表里面的字段
        # exclude = ['username']   除了列表里面的字段其他的都显示
        fields = '__all__'

        # 更改错误提示
        error_messages = {
            'username': {'required': '用户名不能为空'}
        }

        # 更改标签
        labels = {
            'username': '用户名',
            'password': '密码',
            'nickname': '昵称',
            'email': '邮箱',
            'roles': '角色'
        }

        # 插件的使用
        # widgets = {
        #     # 更改文本框的样式
        #     'username': wid.Textarea(attrs={'class': 'c1'})
        # }

    # 定制钩子
    def clean_email(self):
        pass


# 添加用户
def user_add(request):
    if request.method == 'GET':
        model_form = UserModelForm
        return render(request, 'rbac/user_add.html', {'model_form': model_form})

    else:
        model_form = UserModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect('/rbac/users.html')

    return render(request, 'rbac/user_add.html', {"model_form": model_form})


# 编辑
def user_edit(request, pk):
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/rbac/users.html')

    if request.method == 'GET':
        model_form = UserModelForm(instance=obj)
        return render(request, 'rbac/user_edit.html', {'model_form': model_form})

    else:
        model_form = UserModelForm(request.POST, instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/rbac/users.html')


def menus(request):
    menu_list = models.Menu.objects.all()
    return render(request, 'rbac/menus.html', {'menu_list': menu_list})


class MenuModelForm(ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'


def menu_add(request):
    if request.method == 'GET':
        model_form = MenuModelForm
        return render(request, 'rbac/menu_add.html', {'model_form': model_form})

    else:
        model_form = UserModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect('/rbac/menus.html')

    return render(request, 'rbac/menu_add.html', {"model_form": model_form})


def menu_edit(request, pk):
    obj = models.Menu.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/rbac/menus.html')

    if request.method == 'GET':
        model_form = MenuModelForm(instance=obj)
        return render(request, 'rbac/menu_edit.html', {'model_form': model_form})

    else:
        model_form = MenuModelForm(request.POST, instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/rbac/menus.html')


def permissions(request):
    permission_list = models.Permission.objects.all()
    return render(request, 'rbac/permissions.html', {'permission_list': permission_list})


class PermissionModelForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = '__all__'


def permission_add(request):
    if request.method == 'GET':
        model_form = PermissionModelForm
        return render(request, 'rbac/permission_add.html', {'model_form': model_form})

    else:
        model_form = PermissionModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect('/rbac/permissions.html')

    return render(request, 'rbac/permission_add.html', {"model_form": model_form})


def permission_edit(request, pk):
    obj = models.Permission.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/rbac/permissions.html')

    if request.method == 'GET':
        model_form = PermissionModelForm(instance=obj)
        return render(request, 'rbac/permission_edit.html', {'model_form': model_form})

    else:
        model_form = PermissionModelForm(request.POST, instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/rbac/permissions.html')


def roles(request):
    role_list = models.Role.objects.all()
    return render(request, 'rbac/roles.html', {'role_list': role_list})


class RoleModelForm(ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'


def role_add(request):
    if request.method == 'GET':
        model_form = RoleModelForm
        return render(request, 'rbac/role_add.html', {'model_form': model_form})

    else:
        model_form = RoleModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect('/rbac/role.html')

    return render(request, 'rbac/role_add.html', {"model_form": model_form})


def role_edit(request, pk):
    obj = models.Role.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/rbac/roles.html')

    if request.method == 'GET':
        model_form = RoleModelForm(instance=obj)
        return render(request, 'rbac/role_edit.html', {'model_form': model_form})

    else:
        model_form = RoleModelForm(request.POST, instance=obj)
        if model_form.is_valid():
            model_form.save()
        return redirect('/rbac/role.html')
