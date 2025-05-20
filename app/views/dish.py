from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from app.models import Dish, Category
from app.forms import DishForm
from app import db
import os
import json
import uuid
import time
from werkzeug.utils import secure_filename
from PIL import Image
import io

# 创建蓝图
dish_bp = Blueprint('dishes', __name__, url_prefix='/dishes')

def allowed_file(filename):
    """检查文件是否是允许的扩展名"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image(file):
    """保存上传的图片并返回文件路径，同时进行压缩和优化"""
    if file and allowed_file(file.filename):
        start_time = time.time()
        # 确保文件名安全，防止路径遍历攻击
        filename = secure_filename(file.filename)
        # 生成唯一的文件名以防止覆盖
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # 使用Pillow进行图片压缩和优化
        try:
            # 创建一个内存中的副本以避免多次打开文件
            file_content = file.read()
            img = Image.open(io.BytesIO(file_content))
            
            # 保留EXIF信息（如果存在）
            exif = img.info.get('exif')
            
            # 转换为RGB模式（处理RGBA或其他模式）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 限制最大尺寸为1200px（保持纵横比）
            max_size = 1200
            if img.width > max_size or img.height > max_size:
                if img.width > img.height:
                    new_width = max_size
                    new_height = int(img.height * (max_size / img.width))
                else:
                    new_height = max_size
                    new_width = int(img.width * (max_size / img.height))
                
                # 使用LANCZOS重采样方法进行高质量调整大小
                img = img.resize((new_width, new_height), Image.LANCZOS)
                current_app.logger.info(f"图片已调整大小: {new_width}x{new_height}")
                
            # 创建缩略图版本用于列表显示
            thumb_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"thumb_{unique_filename}")
            thumb = img.copy()
            thumb.thumbnail((400, 400), Image.LANCZOS)  # 缩略图最大尺寸为400px
            
            # 保存优化的缩略图
            thumb.save(thumb_path, 'JPEG', quality=80, optimize=True)
            thumb_size = os.path.getsize(thumb_path) / 1024
            current_app.logger.info(f"缩略图大小: {thumb_size:.2f}KB")
            
            # 保存图片，优化质量和文件大小
            img.save(file_path, 'JPEG', quality=85, optimize=True, exif=exif if exif else None)
            
            # 记录处理时间和图片大小
            process_time = time.time() - start_time
            file_size = os.path.getsize(file_path) / 1024  # KB
            current_app.logger.info(f"图片处理耗时: {process_time:.2f}秒, 大小: {file_size:.2f}KB")
            
            # 如果图片仍然大于1MB，进一步降低质量
            if file_size > 1024:  # 大于1MB
                current_app.logger.info("图片过大，进一步优化...")
                lower_quality = 70
                img.save(file_path, 'JPEG', quality=lower_quality, optimize=True)
                new_size = os.path.getsize(file_path) / 1024
                current_app.logger.info(f"优化后大小: {new_size:.2f}KB (质量: {lower_quality}%)")
                
                # 如果还是过大，最后再降低一次质量
                if new_size > 800:  # 还是超过800KB
                    lowest_quality = 60
                    img.save(file_path, 'JPEG', quality=lowest_quality, optimize=True)
                    final_size = os.path.getsize(file_path) / 1024
                    current_app.logger.info(f"最终优化大小: {final_size:.2f}KB (质量: {lowest_quality}%)")
            
            # 返回相对于静态文件夹的路径
            return os.path.join('uploads', unique_filename)
        except Exception as e:
            current_app.logger.error(f"图片处理失败: {str(e)}")
            # 如果图片处理失败，回退到原始保存方法
            with open(file_path, 'wb') as f:
                file.seek(0)
                f.write(file_content)
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
    start_time = time.time()
    form = DishForm()
    # 动态加载分类选项
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        processing_start = time.time()
        current_app.logger.info(f"表单验证耗时: {processing_start - start_time:.2f}秒")
        
        # 处理图片上传
        image_path = None
        if form.image.data:
            img_start = time.time()
            image_path = save_image(form.image.data)
            current_app.logger.info(f"图片保存耗时: {time.time() - img_start:.2f}秒")
        
        # 处理配料数据 - 优化JSON解析
        ingredients = []
        if form.ingredients_data.data:
            ing_start = time.time()
            try:
                ingredients = json.loads(form.ingredients_data.data)
                # 过滤空配料项，提高存储效率
                ingredients = [ing for ing in ingredients if ing.get('name', '').strip() and ing.get('amount', '').strip()]
                current_app.logger.info(f"配料数量: {len(ingredients)}")
            except json.JSONDecodeError as e:
                current_app.logger.error(f"配料JSON解析错误: {str(e)}, 原始数据: {form.ingredients_data.data[:100]}")
            current_app.logger.info(f"配料处理耗时: {time.time() - ing_start:.2f}秒")
        
        dish = Dish(
            name=form.name.data,
            image_path=image_path,
            ingredients=ingredients,
            recipe=form.recipe.data,
            category_id=form.category_id.data
        )
        
        db_start = time.time()
        db.session.add(dish)
        try:
            db.session.commit()
            current_app.logger.info(f"数据库保存耗时: {time.time() - db_start:.2f}秒")
            current_app.logger.info(f"总处理耗时: {time.time() - processing_start:.2f}秒")
            flash('菜品创建成功!', 'success')
            return redirect(url_for('dishes.index'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"数据库保存失败: {str(e)}")
            flash(f'创建菜品失败: {str(e)}', 'danger')
    
    current_app.logger.info(f"创建菜品页面渲染耗时: {time.time() - start_time:.2f}秒")
    return render_template('dishes/form.html', form=form, title='新建菜品')

@dish_bp.route('/<int:id>')
def view(id):
    """查看菜品详情"""
    dish = Dish.query.get_or_404(id)
    return render_template('dishes/view.html', dish=dish)

@dish_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """编辑菜品"""
    start_time = time.time()
    dish = Dish.query.get_or_404(id)
    form = DishForm(obj=dish)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if request.method == 'GET':
        # 填充已有的配料数据到表单
        form.ingredients_data.data = json.dumps(dish.ingredients)
    
    if form.validate_on_submit():
        processing_start = time.time()
        current_app.logger.info(f"表单验证耗时: {processing_start - start_time:.2f}秒")
        
        # 处理图片上传
        if form.image.data:
            # 删除原来的图片
            if dish.image_path:
                try:
                    old_path = os.path.join(current_app.static_folder, dish.image_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                    
                    # 同时删除缩略图
                    old_thumb_path = os.path.join(
                        current_app.static_folder, 
                        'uploads', 
                        f"thumb_{os.path.basename(dish.image_path)}"
                    )
                    if os.path.exists(old_thumb_path):
                        os.remove(old_thumb_path)
                except Exception as e:
                    current_app.logger.error(f"删除旧图片失败: {str(e)}")
            
            # 保存新图片
            img_start = time.time()
            dish.image_path = save_image(form.image.data)
            current_app.logger.info(f"图片保存耗时: {time.time() - img_start:.2f}秒")
        
        # 更新其他字段
        dish.name = form.name.data
        dish.recipe = form.recipe.data
        dish.category_id = form.category_id.data
        
        # 处理配料数据
        if form.ingredients_data.data:
            ing_start = time.time()
            try:
                ingredients = json.loads(form.ingredients_data.data)
                # 过滤空配料项，提高存储效率
                dish.ingredients = [ing for ing in ingredients if ing.get('name', '').strip() and ing.get('amount', '').strip()]
                current_app.logger.info(f"配料数量: {len(dish.ingredients)}")
            except json.JSONDecodeError as e:
                current_app.logger.error(f"配料JSON解析错误: {str(e)}, 原始数据: {form.ingredients_data.data[:100]}")
            current_app.logger.info(f"配料处理耗时: {time.time() - ing_start:.2f}秒")
        
        db_start = time.time()
        try:
            db.session.commit()
            current_app.logger.info(f"数据库保存耗时: {time.time() - db_start:.2f}秒")
            current_app.logger.info(f"总处理耗时: {time.time() - processing_start:.2f}秒")
            flash('菜品更新成功!', 'success')
            return redirect(url_for('dishes.view', id=dish.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"数据库保存失败: {str(e)}")
            flash(f'更新菜品失败: {str(e)}', 'danger')
    
    current_app.logger.info(f"编辑菜品页面渲染耗时: {time.time() - start_time:.2f}秒")
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
