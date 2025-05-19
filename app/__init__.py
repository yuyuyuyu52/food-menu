import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 配置
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_please_change'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:////home/will/food-menu/food_menu.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 最大16MB上传
    )
    
    # 添加自定义Jinja2过滤器
    @app.template_filter('nl2br')
    def nl2br(value):
        if value:
            return value.replace('\n', '<br>')
        return ''
    
    if config:
        app.config.from_mapping(config)
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # 注册蓝图
    from app.views import category_bp, dish_bp, order_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(dish_bp)
    app.register_blueprint(order_bp)
    
    # 在每个请求之前设置now变量
    @app.before_request
    def before_request():
        from flask import g
        from datetime import datetime
        g.now = datetime.utcnow()
    
    # 注册错误处理函数
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理程序"""
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
