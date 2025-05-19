from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from app.models import Dish
from app.forms import OrderForm
from app import db
from collections import Counter

# 创建蓝图
order_bp = Blueprint('orders', __name__, url_prefix='/orders')

@order_bp.route('/select')
def select():
    """选择菜品创建订单"""
    dishes = Dish.query.all()
    return render_template('orders/select.html', dishes=dishes)

@order_bp.route('/review', methods=['POST'])
def review():
    """查看所选菜品并确认订单"""
    form = OrderForm()
    
    selected_dish_ids = request.form.getlist('dish_ids')
    if not selected_dish_ids:
        flash('请选择至少一个菜品', 'warning')
        return redirect(url_for('orders.select'))
    
    # 获取所选菜品信息
    dishes = Dish.query.filter(Dish.id.in_(selected_dish_ids)).all()
    if not dishes:
        flash('未找到所选菜品', 'danger')
        return redirect(url_for('orders.select'))
    
    # 预填充表单
    for dish_id in selected_dish_ids:
        form.dishes.append_entry(dish_id)
    
    return render_template('orders/review.html', form=form, dishes=dishes)

@order_bp.route('/confirm', methods=['POST'])
def confirm():
    """确认订单，显示合并的配料列表和食谱"""
    form = OrderForm()
    
    if form.validate_on_submit():
        dish_ids = [entry.data for entry in form.dishes]
        dishes = Dish.query.filter(Dish.id.in_(dish_ids)).all()
        
        if not dishes:
            flash('未找到所选菜品', 'danger')
            return redirect(url_for('orders.select'))
        
        # 合并并去重配料
        all_ingredients = []
        for dish in dishes:
            all_ingredients.extend(dish.ingredients)
        
        # 对配料进行分组和汇总
        ingredient_counter = Counter()
        for ingredient in all_ingredients:
            key = f"{ingredient['name']}-{ingredient['amount'].split()[-1] if ' ' in ingredient['amount'] else ''}"
            amount = float(ingredient['amount'].split()[0]) if ' ' in ingredient['amount'] else 1
            ingredient_counter[key] += amount
        
        # 格式化合并后的配料列表
        merged_ingredients = []
        for key, amount in ingredient_counter.items():
            name, unit = key.split('-') if '-' in key else (key, '')
            if unit:
                merged_amount = f"{amount} {unit}"
            else:
                merged_amount = str(amount)
            merged_ingredients.append({'name': name, 'amount': merged_amount})
        
        return render_template('orders/confirm.html', 
                              dishes=dishes, 
                              merged_ingredients=merged_ingredients)
    
    flash('表单验证失败', 'danger')
    return redirect(url_for('orders.select'))
