from app import db
import json
from datetime import datetime

class Category(db.Model):
    """分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    dishes = db.relationship('Dish', backref='category', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
