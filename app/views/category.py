from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from app.models import Category, Dish
from app.forms import CategoryForm
from app import db
import os

# 创建蓝图
category_bp = Blueprint('categories', __name__, url_prefix='/categories')

@category_bp.route('/')
def index():
    """显示所有分类"""
    categories = Category.query.all()
    return render_template('categories/index.html', categories=categories)

@category_bp.route('/create', methods=['GET', 'POST'])
def create():
    """创建新分类"""
    # 如果是直接访问此URL，使用传统表单页面
    if request.method == 'GET':
        form = CategoryForm()
        return render_template('categories/form.html', form=form, title='新建分类')
    
    # POST请求，处理表单提交
    # 判断是否为弹窗提交
    if request.form.get('name'):
        # 直接从弹窗中接收名称
        category = Category(name=request.form['name'])
        db.session.add(category)
        try:
            db.session.commit()
            flash('分类创建成功!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'创建分类失败: {str(e)}', 'danger')
        
        # 如果是AJAX请求，返回JSON响应
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=True, category_id=category.id)
        
        return redirect(url_for('categories.index'))
    else:
        # 标准表单处理
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(name=form.name.data)
            db.session.add(category)
            try:
                db.session.commit()
                flash('分类创建成功!', 'success')
                return redirect(url_for('categories.index'))
            except Exception as e:
                db.session.rollback()
                flash(f'创建分类失败: {str(e)}', 'danger')
        
        return render_template('categories/form.html', form=form, title='新建分类')

@category_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """编辑分类"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        form.populate_obj(category)
        try:
            db.session.commit()
            flash('分类更新成功!', 'success')
            return redirect(url_for('categories.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新分类失败: {str(e)}', 'danger')
    
    return render_template('categories/form.html', form=form, category=category, title='编辑分类')

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """删除分类"""
    category = Category.query.get_or_404(id)
    try:
        # 删除该分类下所有菜品的图片
        for dish in category.dishes:
            if dish.image_path:
                try:
                    # 删除原图和缩略图
                    image_path = os.path.join(current_app.static_folder, dish.image_path)
                    thumb_path = image_path.replace(os.path.basename(image_path), f"thumb_{os.path.basename(image_path)}")
                    
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    if os.path.exists(thumb_path):
                        os.remove(thumb_path)
                except Exception as e:
                    current_app.logger.error(f"删除图片失败: {str(e)}")
        
        db.session.delete(category)
        db.session.commit()
        flash('分类删除成功!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除分类失败: {str(e)}', 'danger')
    
    return redirect(url_for('categories.index'))

@category_bp.route('/<int:id>')
def view(id):
    """查看分类详情"""
    category = Category.query.get_or_404(id)
    return render_template('categories/view.html', category=category)
