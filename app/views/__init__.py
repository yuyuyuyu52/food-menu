from app.views.category import category_bp
from app.views.dish import dish_bp
from app.views.order import order_bp

# 创建主页路由
from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """重定向到点菜页面"""
    return redirect(url_for('orders.select'))
