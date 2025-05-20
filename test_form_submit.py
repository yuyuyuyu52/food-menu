#!/usr/bin/env python
# 文件名: test_form_submit.py
# 描述: 测试菜品表单提交功能

import os
import unittest
import tempfile
import json
from app import create_app, db
from app.models import Category, Dish

class DishFormTestCase(unittest.TestCase):
    """测试菜品表单提交功能"""

    def setUp(self):
        """初始化测试环境"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # 禁用CSRF保护以便测试
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # 创建临时数据库
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        
        # 创建静态文件夹
        self.upload_folder = tempfile.mkdtemp()
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder
        
        # 初始化数据库
        db.create_all()
        
        # 创建一个测试分类
        category = Category(name='测试分类')
        db.session.add(category)
        db.session.commit()
        
        self.client = self.app.test_client()

    def tearDown(self):
        """清理测试环境"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)
        
        # 删除上传的文件
        for root, dirs, files in os.walk(self.upload_folder):
            for file in files:
                os.unlink(os.path.join(root, file))
        os.rmdir(self.upload_folder)

    def test_create_dish_without_image(self):
        """测试创建菜品（不含图片）"""
        ingredients = [{'name': '测试配料1', 'amount': '100g'}, {'name': '测试配料2', 'amount': '200g'}]
        
        response = self.client.post('/dishes/create', data={
            'name': '测试菜品',
            'category_id': 1,  # 使用上面创建的分类ID
            'recipe': '测试菜谱内容',
            'ingredients_data': json.dumps(ingredients)
        }, follow_redirects=True)
        
        # 检查是否成功
        self.assertEqual(response.status_code, 200)
        
        # 检查数据库中是否有新创建的菜品
        dish = Dish.query.filter_by(name='测试菜品').first()
        self.assertIsNotNone(dish)
        self.assertEqual(dish.recipe, '测试菜谱内容')
        self.assertEqual(dish.category_id, 1)
        self.assertEqual(len(dish.ingredients), 2)
        self.assertEqual(dish.ingredients[0]['name'], '测试配料1')
        
        print('测试创建菜品（不含图片）: 通过')

    def test_empty_ingredient_filtering(self):
        """测试空配料项过滤功能"""
        # 包含一些空配料项的数据
        ingredients = [
            {'name': '有效配料', 'amount': '100g'},
            {'name': '', 'amount': ''},
            {'name': '  ', 'amount': '200g'},
            {'name': '另一个配料', 'amount': ''}
        ]
        
        response = self.client.post('/dishes/create', data={
            'name': '配料测试菜品',
            'category_id': 1,
            'recipe': '测试配料过滤',
            'ingredients_data': json.dumps(ingredients)
        }, follow_redirects=True)
        
        # 检查是否成功
        self.assertEqual(response.status_code, 200)
        
        # 检查过滤后的配料
        dish = Dish.query.filter_by(name='配料测试菜品').first()
        self.assertIsNotNone(dish)
        # 应该只有第一个有效配料被保存
        self.assertEqual(len(dish.ingredients), 1)
        self.assertEqual(dish.ingredients[0]['name'], '有效配料')
        
        print('测试空配料项过滤功能: 通过')

if __name__ == '__main__':
    unittest.main()
