# api_user (CBV)

```python
post : http://127.0.0.1:8000/site/user
      form = {
        "username"：xxx,
        "password": xxx
      }
get / del : http://127.0.0.1:8000/site/user/user_id
patch : http://127.0.0.1:8000/site/user/user_id?password=xxxx
```

# login (FBV)

```python
post : http://127.0.0.1:8000/site/user
      form = {
        "username"：xxx,
        "password": xxx
      }
```



# logout (FBV)

```
get : http://127.0.0.1:8000/site/user
#删除session
```



# data (CBV)

```
POST: http://127.0.0.1:8000/site/data
    form_data = {
      "key":xxx      #创建需要的参数
    }
get:  http://127.0.0.1:8000/site/data?key=xxxx

```

```
drf-yasg没用,用的postman调试的
docker-compose up  执行pipenv环境依赖配置出问题, 不执行pipenv 也可以在 docker成功运行
写得有点急和乱，有的地方没验证参数是否存在或合理..
```

