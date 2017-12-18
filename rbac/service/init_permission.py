from django.conf import settings
from .. import models


def init_permission(request, user_obj):

    """
    初始化用户权限
    """
    # 获取用户的权限名称、url权限、以及菜单id
    permission_item_list = user_obj.roles.values(
        'permissions__title',
        'permissions__url',
        'permissions__menu_id'
    ).distinct()

    # 用户所有的url权限
    permission_url_list = []

    # 用户菜单列表，里面包含每一项为一个字典，字典里面包含这个菜单下的权限以及权限名称和菜单id
    permission_menu_list = []

    for item in permission_item_list:

        permission_url_list.append(item['permissions__url'])
        if item['permissions__menu_id']:
            temp = {
                'title': item['permissions__title'],
                'url': item['permissions__url'],
                'menu_id': item['permissions__menu_id']
            }
            permission_menu_list.append(temp)

    # 所有的菜单
    menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))

    # 将权限列表写入session
    request.session[settings.SESSION_PERMISSION_MENU_URL_KEY] = {
        settings.PERMISSION_URL_KEY: permission_url_list,
        settings.ALL_MENU: menu_list,
        settings.PERMISSION_MENU_KEY: permission_menu_list
    }
