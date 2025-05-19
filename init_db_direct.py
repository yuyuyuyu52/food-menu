import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

# 创建一个简单的Flask应用和SQLAlchemy实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/will/food-menu/food_menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义模型
class Category(db.Model):
    """分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    dishes = db.relationship('Dish', backref='category', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Dish(db.Model):
    """菜品模型"""
    __tablename__ = 'dishes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    ingredients_json = db.Column(db.Text, nullable=False, default='[]')
    recipe = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def ingredients(self):
        """获取配料列表"""
        return json.loads(self.ingredients_json)
        
    @ingredients.setter
    def ingredients(self, ingredients):
        """设置配料列表"""
        self.ingredients_json = json.dumps(ingredients)

# 创建数据库表
with app.app_context():
    db.drop_all()
    db.create_all()
    
    # 创建分类
    categories = [
        Category(name="主食"),
        Category(name="肉类"),
        Category(name="素菜"),
        Category(name="汤类"),
        Category(name="甜点")
    ]
    db.session.add_all(categories)
    db.session.commit()
    
    # 创建菜品
    dishes = [
        Dish(
            name="香菇青菜炒饭",
            ingredients=[
                {"name": "米饭", "amount": "2 碗"},
                {"name": "香菇", "amount": "100 克"},
                {"name": "青菜", "amount": "200 克"},
                {"name": "鸡蛋", "amount": "2 个"},
                {"name": "食用油", "amount": "2 勺"},
                {"name": "盐", "amount": "适量"},
                {"name": "酱油", "amount": "1 勺"}
            ],
            recipe="1. 将米饭提前煮好，最好放凉备用\n2. 香菇切片，青菜切段\n3. 热锅倒油，炒散鸡蛋盛出\n4. 锅中加油，炒香香菇，加入青菜一起炒熟\n5. 加入米饭翻炒均匀，再加入鸡蛋，调入盐和酱油\n6. 大火快速翻炒均匀即可出锅",
            category_id=1
        ),
        Dish(
            name="红烧肉",
            ingredients=[
                {"name": "五花肉", "amount": "500 克"},
                {"name": "生姜", "amount": "30 克"},
                {"name": "大蒜", "amount": "4 瓣"},
                {"name": "八角", "amount": "2 个"},
                {"name": "干辣椒", "amount": "2 个"},
                {"name": "酱油", "amount": "3 勺"},
                {"name": "料酒", "amount": "2 勺"},
                {"name": "冰糖", "amount": "30 克"},
                {"name": "食用油", "amount": "2 勺"}
            ],
            recipe="1. 五花肉切成4厘米见方的块\n2. 锅中倒入清水，放入肉块，煮开，撇去浮沫，捞出肉块\n3. 锅中倒油，放入冰糖，小火熬至糖色\n4. 放入肉块煸炒至表面金黄\n5. 加入姜、蒜、八角、干辣椒，翻炒出香味\n6. 加入酱油、料酒，加水没过肉块\n7. 大火烧开后转小火焖煮1小时\n8. 开大火收汁即可",
            category_id=2
        ),
        Dish(
            name="西红柿蛋汤",
            ingredients=[
                {"name": "西红柿", "amount": "2 个"},
                {"name": "鸡蛋", "amount": "3 个"},
                {"name": "葱", "amount": "2 根"},
                {"name": "盐", "amount": "适量"},
                {"name": "鸡精", "amount": "适量"},
                {"name": "胡椒粉", "amount": "适量"},
                {"name": "香油", "amount": "少许"}
            ],
            recipe="1. 西红柿洗净，切块\n2. 葱洗净切花\n3. 鸡蛋打散\n4. 锅中倒入适量清水，水开后放入西红柿块\n5. 煮至西红柿软烂，调入适量盐\n6. 将打散的鸡蛋沿锅边缓缓倒入，用筷子搅动\n7. 撒入葱花、鸡精、胡椒粉\n8. 滴入几滴香油即可",
            category_id=4
        )
    ]
    db.session.add_all(dishes)
    db.session.commit()
    
    print("=================================")
    print("数据库初始化成功！")
    print("已创建分类:", Category.query.count())
    print("已创建菜品:", Dish.query.count())
    print("=================================")
