"""注册 Tortoise ORM 生命周期"""
from tortoise.contrib.fastapi import register_tortoise
from app.config import TORTOISE_ORM

# 注册数据库
def register_db(app):
    # 注册 Tortoise ORM 到 FastAPI 应用
    # app：FastAPI 应用实例
    # config：Tortoise ORM 配置
    # generate_schemas：是否生成数据库表结构
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False
    )