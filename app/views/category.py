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
