from app import db
import json
from datetime import datetime
import time

def local_now():
    """返回当前的本地时间，而不是UTC时间"""
    return datetime.now()

class Category(db.Model):
    """分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    dishes = db.relationship('Dish', backref='category', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=local_now)
    updated_at = db.Column(db.DateTime, default=local_now, onupdate=local_now)
    
    def __repr__(self):
        return f'<Category {self.name}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dishes_count': len(self.dishes)
        }

class Dish(db.Model):
    """菜品模型"""
    __tablename__ = 'dishes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    ingredients_json = db.Column(db.Text, nullable=False, default='[]')
    recipe = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=local_now)
    updated_at = db.Column(db.DateTime, default=local_now, onupdate=local_now)
    
    # 多对多关系
    orders = db.relationship('Order', secondary='order_dishes', back_populates='dishes')
    
    @property
    def ingredients(self):
        """获取配料列表"""
        return json.loads(self.ingredients_json)
        
    @ingredients.setter
    def ingredients(self, ingredients):
        """设置配料列表"""
        self.ingredients_json = json.dumps(ingredients)
    
    def __repr__(self):
        return f'<Dish {self.name}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_path': self.image_path,
            'ingredients': self.ingredients,
            'recipe': self.recipe,
            'category_id': self.category_id,
            'category_name': self.category.name
        }

# 订单和菜品的关联表
order_dishes = db.Table('order_dishes',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
)

class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)  # 订单名称，可选
    merged_ingredients_json = db.Column(db.Text, nullable=False, default='[]')  # 合并的配料列表
    ingredients_status_json = db.Column(db.Text, nullable=False, default='[]')  # 配料完成状态
    created_at = db.Column(db.DateTime, nullable=False, default=local_now)
    
    # 多对多关系
    dishes = db.relationship('Dish', secondary='order_dishes', back_populates='orders')
    
    @property
    def merged_ingredients(self):
        """获取合并的配料列表"""
        return json.loads(self.merged_ingredients_json)
        
    @merged_ingredients.setter
    def merged_ingredients(self, ingredients):
        """设置合并的配料列表"""
        self.merged_ingredients_json = json.dumps(ingredients)
    
    @property
    def ingredients_status(self):
        """获取配料完成状态"""
        return json.loads(self.ingredients_status_json)
        
    @ingredients_status.setter
    def ingredients_status(self, status):
        """设置配料完成状态"""
        self.ingredients_status_json = json.dumps(status)
    
    def __repr__(self):
        return f'<Order {self.id}>'
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'merged_ingredients': self.merged_ingredients,
            'dishes': [dish.to_dict() for dish in self.dishes],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
