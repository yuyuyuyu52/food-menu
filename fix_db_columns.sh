#!/bin/bash
# 此脚本用于修复服务器上的数据库结构问题
# 它将检查并添加缺失的列

set -e

echo "=== 开始修复数据库结构 ==="

# 确定当前目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
echo "=== 激活虚拟环境 ==="
source venv/bin/activate

# 创建Python脚本来修复数据库
cat > fix_db.py << 'EOF'
#!/usr/bin/env python3
import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

# 创建一个简单的Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/food_menu.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化SQLAlchemy和Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def check_column_exists(table, column):
    """检查表中是否存在特定列"""
    conn = sqlite3.connect('instance/food_menu.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    conn.close()
    
    column_names = [col[1] for col in columns]
    return column in column_names

def add_missing_columns():
    """添加缺失的列"""
    conn = sqlite3.connect('instance/food_menu.db')
    cursor = conn.cursor()
    
    # 检查orders表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    if not cursor.fetchone():
        print("orders表不存在，请先运行数据库迁移")
        conn.close()
        return False
    
    # 检查并添加ingredients_status_json列
    if not check_column_exists('orders', 'ingredients_status_json'):
        print("添加orders.ingredients_status_json列...")
        cursor.execute("ALTER TABLE orders ADD COLUMN ingredients_status_json TEXT NOT NULL DEFAULT '[]'")
        print("已添加orders.ingredients_status_json列")
    else:
        print("orders.ingredients_status_json列已存在")
    
    # 检查是否有其他缺失的列
    missing_columns = []
    
    # 检查categories表的created_at和updated_at
    if not check_column_exists('categories', 'created_at'):
        missing_columns.append(("categories", "created_at", "DATETIME"))
    
    if not check_column_exists('categories', 'updated_at'):
        missing_columns.append(("categories", "updated_at", "DATETIME"))
    
    # 检查dishes表的created_at和updated_at
    if not check_column_exists('dishes', 'created_at'):
        missing_columns.append(("dishes", "created_at", "DATETIME"))
    
    if not check_column_exists('dishes', 'updated_at'):
        missing_columns.append(("dishes", "updated_at", "DATETIME"))
    
    # 检查orders表的created_at
    if not check_column_exists('orders', 'created_at'):
        missing_columns.append(("orders", "created_at", "DATETIME"))
    
    # 添加缺失的列
    for table, column, dtype in missing_columns:
        print(f"添加{table}.{column}列...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype}")
        print(f"已添加{table}.{column}列")
    
    conn.commit()
    conn.close()
    
    print("所有列都已检查并修复")
    return True

def main():
    """主函数"""
    print("检查并修复数据库表结构...")
    if add_missing_columns():
        print("数据库修复成功完成")
        return 0
    else:
        print("数据库修复失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

# 执行修复脚本
echo "=== 执行数据库修复脚本 ==="
python fix_db.py

echo "=== 数据库修复完成 ==="

# 运行数据库迁移以确保Schema是最新的
echo "=== 运行数据库迁移 ==="
export FLASK_APP=app.py
flask db stamp head
flask db migrate -m "fix missing columns"
flask db upgrade

echo "=== 数据库迁移完成 ==="
echo "=== 数据库修复过程全部完成 ==="
