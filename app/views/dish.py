from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from app.models import Dish, Category
from app.forms import DishForm
from app import db
import os
import json
import uuid
from werkzeug.utils import secure_filename

# 创建蓝图
dish_bp = Blueprint('dishes', __name__, url_prefix='/dishes')

def allowed_file(filename):
    """检查文件是否是允许的扩展名"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image(file):
    """保存上传的图片并返回文件路径"""
    if file and allowed_file(file.filename):
        # 确保文件名安全，防止路径遍历攻击
        filename = secure_filename(file.filename)
        # 生成唯一的文件名以防止覆盖
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        # 返回相对于静态文件夹的路径
        return os.path.join('uploads', unique_filename)
    return None

@dish_bp.route('/')
def index():
    """显示所有菜品"""
    category_id = request.args.get('category_id', type=int)
    
    if category_id:
        dishes = Dish.query.filter_by(category_id=category_id).all()
        category = Category.query.get_or_404(category_id)
        return render_template('dishes/index.html', dishes=dishes, category=category)
    else:
        dishes = Dish.query.all()
        return render_template('dishes/index.html', dishes=dishes)

@dish_bp.route('/create', methods=['GET', 'POST'])
def create():
    """创建新菜品"""
    form = DishForm()
    # 动态加载分类选项
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        # 处理图片上传
        image_path = None
        if form.image.data:
            image_path = save_image(form.image.data)
        
        # 处理配料数据
        ingredients = []
        if form.ingredients_data.data:
            ingredients = json.loads(form.ingredients_data.data)
        
        dish = Dish(
            name=form.name.data,
            image_path=image_path,
            ingredients=ingredients,
            recipe=form.recipe.data,
            category_id=form.category_id.data
        )
        
        db.session.add(dish)
        try:
            db.session.commit()
            flash('菜品创建成功!', 'success')
            return redirect(url_for('dishes.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'创建菜品失败: {str(e)}', 'danger')
    
    return render_template('dishes/form.html', form=form, title='新建菜品')

@dish_bp.route('/<int:id>')
def view(id):
    """查看菜品详情"""
    dish = Dish.query.get_or_404(id)
    return render_template('dishes/view.html', dish=dish)

@dish_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """编辑菜品"""
    dish = Dish.query.get_or_404(id)
    form = DishForm(obj=dish)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if request.method == 'GET':
        # 填充已有的配料数据到表单
        form.ingredients_data.data = json.dumps(dish.ingredients)
    
    if form.validate_on_submit():
        # 处理图片上传
        if form.image.data:
            # 删除原来的图片
            if dish.image_path:
                try:
                    old_path = os.path.join(current_app.static_folder, dish.image_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception as e:
                    current_app.logger.error(f"删除旧图片失败: {str(e)}")
            
            # 保存新图片
            dish.image_path = save_image(form.image.data)
        
        # 更新其他字段
        dish.name = form.name.data
        dish.recipe = form.recipe.data
        dish.category_id = form.category_id.data
        
        # 处理配料数据
        if form.ingredients_data.data:
            dish.ingredients = json.loads(form.ingredients_data.data)
        
        try:
            db.session.commit()
            flash('菜品更新成功!', 'success')
            return redirect(url_for('dishes.view', id=dish.id))
        except Exception as e:
            db.session.rollback()
            flash(f'更新菜品失败: {str(e)}', 'danger')
    
    return render_template('dishes/form.html', form=form, dish=dish, title='编辑菜品')

@dish_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """删除菜品"""
    dish = Dish.query.get_or_404(id)
    
    # 删除关联的图片文件
    if dish.image_path:
        try:
            file_path = os.path.join(current_app.static_folder, dish.image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            current_app.logger.error(f"删除图片失败: {str(e)}")
    
    try:
        db.session.delete(dish)
        db.session.commit()
        flash('菜品删除成功!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除菜品失败: {str(e)}', 'danger')
    
    return redirect(url_for('dishes.index'))
