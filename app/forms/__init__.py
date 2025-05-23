from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FieldList, FormField, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
import json

class CategoryForm(FlaskForm):
    """分类表单"""
    name = StringField('分类名称', validators=[DataRequired(), Length(min=2, max=100)])
    save_button = SubmitField('保存')  # 重命名为save_button

class IngredientForm(FlaskForm):
    """配料表单"""
    name = StringField('名称', validators=[DataRequired()])
    amount = StringField('数量', validators=[DataRequired()])

class DishForm(FlaskForm):
    """菜品表单"""
    name = StringField('菜品名称', validators=[DataRequired(), Length(min=2, max=100)])
    image = FileField('菜品图片', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许上传图片!')
    ])
    category_id = SelectField('分类', coerce=int, validators=[DataRequired()])
    recipe = TextAreaField('烹饪方法', validators=[Optional()])
    ingredients_data = HiddenField('配料数据')
    save_button = SubmitField('保存')  # 重命名submit为save_button，避免与表单submit方法冲突

class OrderForm(FlaskForm):
    """订单表单"""
    name = StringField('订单名称', validators=[Optional(), Length(max=100)])
    dishes = FieldList(HiddenField('菜品ID'), min_entries=1)
    save_button = SubmitField('确认订单')  # 重命名为save_button
