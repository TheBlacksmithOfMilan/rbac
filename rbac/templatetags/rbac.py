from django.template import Library
import re
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import mark_safe
import os

register = Library()


def process_menu_data(request):
    """
    生成菜单相关数据
    """
    menu_permission_url_list = request.session.get(settings.SESSION_PERMISSION_MENU_URL_KEY)
    # print(menu_permission_url_list)
    permission_menu_url_list = menu_permission_url_list['permission_menu_list']
    menu_list = menu_permission_url_list['all_menu']
    permission_list = menu_permission_url_list['permission_url']

    # menu_list如下
    """
    [
    {'id': 1, 'caption': '用户管理', 'parent_id': None}, 
    {'id': 2, 'caption': '订单管理', 'parent_id': 1}
    ]
    """

    all_menu_dict = {}
    for item in menu_list:
        item['children'] = []
        item['status'] = False  # 是否显示当前菜单
        item['open'] = False  # 是否默认展开
        all_menu_dict[item['id']] = item

    # print(all_menu_dict)
    """
    {
    1: {'id': 1, 'caption': '用户管理', 'parent_id': None, 'children': [], 'status': False, 'open': False}, 
    2: {'id': 2, 'caption': '订单管理', 'parent_id': 1, 'children': [], 'status': False, 'open': False}
    }
    """
    # print(permission_menu_url_list)
    """
    [
    {'title': '权限1', 'url': '/index/', 'menu_id': 1}
    ]
    """
    # 循环权限信息，将权限信息添加到父menu中
    for per in permission_menu_url_list:
        per['status'] = True
        pattern = settings.URL_REGEX.format(per['url'])
        if re.match(pattern, request.path_info):
            per['open'] = True
        else:
            per['open'] = False

        all_menu_dict[per['menu_id']]['children'].append(per)

        pid = per['menu_id']

        while pid:
            all_menu_dict[pid]['status'] = True  # 更改当前权限的父菜单的状态为True
            pid = all_menu_dict[pid]['parent_id']  # 更改pid为父菜单的父菜单，继续循环，直到没有父菜单

        p_pid = per['menu_id']

        while p_pid:
            all_menu_dict[p_pid]['open'] = True
            p_pid = all_menu_dict[p_pid]['parent_id']

    # print(all_menu_dict)
    """
    {
        1: {
            'id': 1, 
            'caption': '用户管理', 
            'parent_id': None, 
            'children': [{'title': '权限1', 'url': '/index/', 'menu_id': 1, 'open': False}], 
            'status': True, 
            'open': True
            }, 
        2: {
            'id': 2, 
            'caption': '订单管理', 
            'parent_id': 1, 
            'children': [], 
            'status': False, 
            'open': False
            }
    }
    """

    # 将菜单添加到父菜单的children里面去
    result = []
    for k, v in all_menu_dict.items():
        if not v.get('parent_id'):
            result.append(v)
        else:
            p = v.get('parent_id')
            all_menu_dict[p]['children'].append(v)

    # print(result)
    """
    [
        {
            'id': 4, 
            'caption': '菜单1', 
            'parent_id': None, 
            'children': [
                {'id': 6, 'caption': '菜单3', 'parent_id': 4, 'children': [], 'status': False, 'open': False}
                ], 
            'status': False, 
            'open': False
        }, 
        {
            'id': 5, 
            'caption': '菜单2', 
            'parent_id': None, 
            'children': [
                {'title': '权限2', 'url': '/index/', 'menu_id': 5, 'open': False}
                ], 
            'status': True, 
            'open': True}
    ]
    """
    return result


def process_menu_html(menu_list):
    tpl1 = """
                <div class='rbac-menu-item'>
                    <div class='rbac-menu-header'>{0}</div>
                    <div class='rbac-menu-body {2}'>{1}</div>
                </div>
            """
    tpl2 = """
                <a href='{0}' class='{1}'>{2}</a>
            """

    html = ""

    for item in menu_list:
        # print(item)
        if not item.get('status'):
            continue
        if item.get('url'):
            # 权限
            html += tpl2.format(item['url'], "rbac-active" if item['open'] else "", item['title'])
            # print(html)
        else:
            # 菜单
            html += tpl1.format(item['caption'], process_menu_html(item['children']),
                                "" if item['open'] else "rbac-hide")

    return html


@register.simple_tag
def menus(request):
    """
    生成菜单
    """
    result = process_menu_data(request)
    # print(result)
    html = process_menu_html(result)
    return mark_safe(html)


@register.simple_tag
def rbac_css():
    file_path = os.path.join('rbac', 'theme', 'rbac.css')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题CSS文件不存在')


@register.simple_tag
def rbac_js():
    file_path = os.path.join('rbac', 'theme', 'rbac.js')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题JavaScript文件不存在')
