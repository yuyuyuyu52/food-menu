# 食品菜单应用

一个使用 Flask 构建的食品菜单和食谱管理应用程序，允许用户创建食品分类和菜品，并提供基于所选菜品的配料整合功能。

## 主要功能

- 分类管理：增加、修改、删除食品分类
- 菜品管理：增加、修改、删除菜品，包括名称、图片、配料和烹饪步骤
- 订单流程：用户可选择多个菜品，系统会自动合并所需配料并显示烹饪步骤
- 响应式设计：使用 Bootstrap 5 确保在各种设备上都有良好的用户体验

## 技术栈

- **后端**：Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- **前端**：Bootstrap 5, Jinja2, JavaScript, jQuery
- **数据库**：SQLite (开发环境)，可扩展到其他数据库

## 安装与设置

### 前提条件

- Python 3.8+
- pip (Python 包管理工具)

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/food-menu.git
cd food-menu
```

2. 创建并激活虚拟环境

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. 安装依赖项

```bash
pip install -r requirements.txt
```

4. 初始化数据库与迁移

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

5. 添加测试数据 (可选)

```bash
flask seed-db
```

6. 启动应用

```bash
flask run
```

应用将在 http://127.0.0.1:5000/ 上运行。

## 项目结构

```
food-menu/
├── app/                    # 应用程序主目录
│   ├── __init__.py         # 应用工厂和配置
│   ├── forms/              # 表单模块
│   ├── models/             # 数据模型
│   ├── static/             # 静态文件
│   │   ├── css/            # CSS 样式表
│   │   ├── js/             # JavaScript 文件
│   │   └── uploads/        # 上传的图片
│   ├── templates/          # Jinja2 模板
│   └── views/              # 视图蓝图
├── migrations/             # 数据库迁移目录
├── app.py                  # 应用入口点
├── requirements.txt        # 项目依赖
└── README.md               # 项目文档
```

## 数据库模型

- **Category**: 菜品分类
  - id: 唯一标识符
  - name: 分类名称

- **Dish**: 菜品
  - id: 唯一标识符
  - name: 菜品名称
  - image_path: 菜品图片路径
  - ingredients_json: 配料列表 (JSON 格式)
  - recipe: 烹饪步骤
  - category_id: 所属分类 (外键)

## 路由结构

- `/`: 主页，重定向到分类列表
- `/categories/`: 分类列表
- `/categories/create`: 创建分类
- `/categories/<id>/edit`: 编辑分类
- `/categories/<id>/delete`: 删除分类
- `/dishes/`: 菜品列表
- `/dishes/create`: 创建菜品
- `/dishes/<id>`: 查看菜品详情
- `/dishes/<id>/edit`: 编辑菜品
- `/dishes/<id>/delete`: 删除菜品
- `/orders/select`: 选择菜品
- `/orders/review`: 查看所选菜品
- `/orders/confirm`: 确认并显示合并后的配料和烹饪步骤

## 开发指南

- 使用 `flask db migrate` 创建新的迁移脚本
- 使用 `flask db upgrade` 应用迁移
- 应用程序使用应用工厂模式，便于扩展和测试

## 许可

本项目基于 MIT 许可发布。
