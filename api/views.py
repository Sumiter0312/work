
import re
import random

from django.views import View
from api import models
from django.http.response import JsonResponse
from rest_framework import status
from django.forms.models import model_to_dict



class UserView(View):
    """
    请求方式:
                http://127.0.0.1:8000/site/user
    """
    def return_exist(self,obj):
        if not obj:
            res = JsonResponse({
                "code": 0,
                "msg": "不存在该用户"
            })
            res.status_code = status.HTTP_401_UNAUTHORIZED
            return res

    def post(self,request,pk):
        """
            创建用户
        """

        username = request.POST.get("username")
        pwd = request.POST.get("password")
        username_regex = r"[a-zA-Z]{10,}"
        pwd_regex = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[$@$!%*?&.])[A-Za-z\d]{1,6}"

        user_match = re.findall(username_regex,username)
        pwd_match = re.findall(pwd_regex,pwd)

        if user_match and pwd_match:
            models.User.objects.create(username=username,password=pwd)
            res = JsonResponse({
                "code": 1,
                "msg": "创建成功"
            })
            res.status_code = status.HTTP_201_CREATED
            return res


        res = JsonResponse({
            "code": 0,
            "msg": "创建失败"
        })
        res.status_code = status.HTTP_200_OK
        return res



    def get(self,request,pk):
        """
            获取
            请求方式:
                http://127.0.0.1:8000/site/user/(?P<id>\d+)
        """
        obj = models.User.objects.filter(id=pk)
        res = self.return_exist(obj)
        if res:return res

        res = JsonResponse({
            "code": 1,
            "msg": model_to_dict(obj.first(),fields=["username","password"])
        })
        res.status_code = status.HTTP_200_OK
        return res


    def delete(self,request,pk):
        """
            删除
            请求方式:
                http://127.0.0.1:8000/site/user/(?P<id>\d+)
        """
        obj = models.User.objects.filter(id=pk)
        res = self.return_exist(obj)
        if res:return res

        obj.delete()
        res = JsonResponse({
            "code": 1,
            "msg": "删除成功"
        })
        res.status_code = status.HTTP_200_OK
        return res

    def patch(self,request,pk):
        """
            修改用户密码
            请求方式:
                http://127.0.0.1:8000/site/user/(?P<id>\d+)?pwd=xxxx
        """
        user_id = request.session.get("user_id")
        pwd = request.GET.get("pwd")

        # 传值为空
        if not pk or not pwd:
            res = JsonResponse({
                "code": 0,
                "msg": "穿值为空"
            })
            res.status_code = status.HTTP_401_UNAUTHORIZED
            return res

        # 客户端传递参数有失
        if int(user_id) != int(pk):
            res = JsonResponse({
                "code": 0,
                "msg": "修改失败"
            })
            res.status_code = status.HTTP_401_UNAUTHORIZED
            return res

        query = models.User.objects.filter(id=pk)

        res = self.return_exist(query)
        if res:return res

        #保存
        obj = query.first()
        obj.password = pwd
        obj.save()

        res = JsonResponse({
            "code": 1,
            "msg": "修改成功"
        })
        res.status_code = status.HTTP_200_OK
        return res

def login(request):
    """
    请求方式:
                http://127.0.0.1:8000/site/login
    """


    if request.method != "POST":
        res = JsonResponse({
            "code":0,
            "msg":"请求方法不被允许"
        })
        res.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return res

    user = request.POST.get("username")
    pwd = request.POST.get("password")
    obj = models.User.objects.filter(username=user,password=pwd)

    if not obj:
        res = JsonResponse({
            "code":0,
            "msg":"不存在该obj"
        })
        res.status_code = status.HTTP_401_UNAUTHORIZED
        return res

    request.session["user_id"] = obj.first().pk

    res = JsonResponse({
        "code":1,
        "msg":"登录成功"
    })
    res.status_code = status.HTTP_201_CREATED
    return res

def logout(request):
    """
        请求方式:
                http://127.0.0.1:8000/site/logout
    """
    if request.method != "GET":
        res = JsonResponse({
            "code":0,
            "msg":"请求方法不被允许"
        })
        res.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return res

    request.session.delete()
    res = JsonResponse({
        "code": 1,
        "msg": "请求成功"
    })
    res.status_code = status.HTTP_200_OK
    return res

class DataView(View):
    """
        中间件校验是否登录
    """

    def create(self):
        """
        随机生成句子
        """
        str = ""
        dic = {
            "person":['小明',"小红","小驴","小猪","小野马","小王八","小杂总","小刘波"],
            "status":["精神的","亢奋的","安稳的","安全的","惬意的","舒适的"],
            "where":["在酒吧","在学校","在楼上","在网吧","在地上","在家里"],
            "what":["吃饭","洗澡","做作业","学习","打游戏","哭泣","玩耍","喝酒","抽烟"]
        }
        for v in dic.values():
            str += v[random.randint(0,len(v)-1)]

        return str

    def post(self,request):
        """
        随机创建数据
        0-10
            小于7.5 属于3/4概率 ,
            反之 1/4
        请求方式:
                http://127.0.0.1:8000/site/data
        """
        str = request.POST.get("key")


        for i in range(20):
            number = random.randint(1, 10)
            res = self.create()
            if number<=7.5:
                res = self.create()+str
            lens  = len(res)
            # 有些耗费性能,应该批量创建
            models.Data.objects.create(str=res, len=lens)

        res = JsonResponse({
            "code":1,
            "msg":"创建成功",
        })
        res.status_code = status.HTTP_201_CREATED
        return res

    def get(self,request):
        """
        获取数据个数
        请求方式:
                http://127.0.0.1:8000/site/data
        """
        key = request.GET.get("key")
        count = models.Data.objects.filter(str__contains=key,len__gt=10)
        print(count)
        # 没查到
        if not count:
            res = JsonResponse({
                "code": 0,
                "msg":"结果为空"
            })
            res.status_code = status.HTTP_200_OK
            return res

        res = JsonResponse({
            "code": 1,
            "count":len(count)
        })

        res.status_code = status.HTTP_200_OK
        return res
