import sqlite3

conn = sqlite3.connect('/home/will/food-menu/instance/food_menu.db')
cursor = conn.cursor()

# 获取所有表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("数据库中的表:")
for table in tables:
    print(f"- {table[0]}")

# 如果有'categories'表，获取其内容
if ('categories',) in tables:
    print("\n分类表内容:")
    cursor.execute("SELECT * FROM categories;")
    categories = cursor.fetchall()
    if categories:
        for category in categories:
            print(category)
    else:
        print("分类表为空")
else:
    print("\n分类表不存在")

conn.close()
