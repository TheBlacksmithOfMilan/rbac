from django.db import models


# Create your models here.
class Menu(models.Model):
    """
    菜单表
    """
    caption = models.CharField(max_length=32)   # 菜单标题
    parent = models.ForeignKey('Menu', null=True, blank=True)    # 父菜单, 可以为空, 在admin可以显示

    def __str__(self):
        p = self.parent
        caption_list = [self.caption]
        while p:
            caption_list.insert(0, p.caption)
            p = p.parent

        return '-'.join(caption_list)


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32)  # 权限标题
    url = models.CharField(max_length=255)   # url
    menu = models.ForeignKey('Menu', null=True, blank=True)

    def __str__(self):
        return '%s---%s' % (self.title, self.menu)


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.username
