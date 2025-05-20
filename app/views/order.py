from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from app.models import Dish, Category, Order
from app.forms import OrderForm
from app import db
from collections import Counter

# 创建蓝图
order_bp = Blueprint('orders', __name__, url_prefix='/orders')

@order_bp.route('/select')
def select():
    """选择菜品创建订单"""
    dishes = Dish.query.all()
    categories = Category.query.all()
    return render_template('orders/select.html', dishes=dishes, categories=categories)

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
        
        # 初始化配料完成状态，默认都设为未完成
        # ingredients_status 保存已经选中的配料名称列表
        ingredients_status = []
        
        # 保存订单到数据库
        order_name = form.name.data if hasattr(form, 'name') and form.name.data else f"订单 {len(dishes)}个菜品"
        new_order = Order(
            name=order_name, 
            merged_ingredients=merged_ingredients,
            ingredients_status=ingredients_status
        )
        new_order.dishes = dishes
        
        try:
            db.session.add(new_order)
            db.session.commit()
            flash('订单已保存！', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'保存订单失败: {str(e)}', 'danger')
        
        return render_template('orders/confirm.html', 
                              order=new_order,
                              dishes=dishes, 
                              merged_ingredients=merged_ingredients)
    
    flash('表单验证失败', 'danger')
    return redirect(url_for('orders.select'))

@order_bp.route('/history')
def history():
    """查看订单历史"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders/history.html', orders=orders)

@order_bp.route('/view/<int:id>')
def view(id):
    """查看订单详情"""
    order = Order.query.get_or_404(id)
    return render_template('orders/view.html', order=order)

@order_bp.route('/api/ingredients-status/<int:order_id>', methods=['GET'])
def get_ingredients_status(order_id):
    """获取订单配料状态"""
    order = Order.query.get_or_404(order_id)
    return jsonify(order.ingredients_status)

@order_bp.route('/api/ingredients-status/<int:order_id>', methods=['POST'])
def update_ingredients_status(order_id):
    """更新订单配料状态"""
    order = Order.query.get_or_404(order_id)
    
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400
        
    status = request.get_json()
    
    try:
        order.ingredients_status = status
        db.session.commit()
        return jsonify({"success": True, "message": "配料状态已更新"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
