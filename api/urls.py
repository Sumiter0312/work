
from django.conf.urls import url
from api.views import UserView,DataView,login,logout

urlpatterns = [
    # "用户crud"
    url(r'user/(?P<pk>\d+)?$', UserView.as_view()),
    # "创建/获取数据"
    url(r"data",DataView.as_view()),
    # "登录注销"
    url(r"login",login,name="login"),
    url(r"logout",logout),
]
