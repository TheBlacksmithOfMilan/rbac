from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import re
from django.shortcuts import render, redirect, HttpResponse


# 定义中间件
class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        for url in settings.PASS_URL_LIST:
            if re.match(url, request.path_info):
                return None
        permission_url_list = request.session.get(settings.SESSION_PERMISSION_MENU_URL_KEY)['permission_url']

        if not permission_url_list:
            return redirect(settings.LOGIN_URL)

        flag = False
        for db_url in permission_url_list:
            pattern = settings.URL_REGEX.format(db_url)
            if re.match(pattern, request.path_info):
                flag = True
                break

        if not flag:
            if settings.DEBUG:
                url_html = '<br/>'.join(permission_url_list)
                return HttpResponse('无权访问!<br/>请访问：%s' % url_html)
            else:
                return HttpResponse('无权访问')
