#!/usr/bin/env python3
# filepath: /home/will/food-menu/create_db.py
import os
from app import create_app, db
from app.models import Category, Dish

app = create_app()

with app.app_context():
    # 确保instance目录存在
    os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)
    
    # 创建所有表
    db.create_all()
    
    # 如果没有任何分类，添加一些基本分类
    if Category.query.count() == 0:
        categories = [
            Category(name='主食'),
            Category(name='肉类'),
            Category(name='素菜'),
            Category(name='汤品'),
            Category(name='甜点')
        ]
        db.session.add_all(categories)
        db.session.commit()
        print("已创建基础分类")
    
    print("数据库初始化完成!")
