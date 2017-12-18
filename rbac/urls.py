
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^users.html/$', views.users),
    url(r'^menus.html/$', views.menus),
    url(r'^permissions.html/$', views.permissions),
    url(r'^roles.html/$', views.roles),
    url(r'^user/add.html/$', views.user_add),
    url(r'^menu/menu_add.html/$', views.menu_add),
    url(r'^role/role_add.html/$', views.role_add),
    url(r'^permission/permission_add.html/$', views.permission_add),
    url(r'^user/edit/(\d+).html/$', views.user_edit),
    url(r'^menu/menu_edit/(\d+).html/$', views.menu_edit),
    url(r'^permission/permission_edit/(\d+).html/$', views.permission_edit),
    url(r'^role/role_edit/(\d+).html/$', views.role_edit),
]
