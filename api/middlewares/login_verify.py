import json


from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse
from rest_framework import status

class LoginMD(MiddlewareMixin):
    """
    登录检测
    """
    def process_view(self, request, callback, callback_args, callback_kwargs):
       if callback.__name__ == "DataView":
          id = request.session.get("user_id")
          if not id:
             res = JsonResponse({
                  "code":0,
                  "msg":"请登录"
              })
             res.status_code = status.HTTP_302_FOUND
             return res


