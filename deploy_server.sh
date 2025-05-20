#!/bin/bash
# 部署脚本，用于在服务器上初始化和启动应用

set -e  # 脚本中的任何错误将导致脚本终止

echo "=== 开始部署食品菜单应用 ==="

# 确定当前目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "=== 创建虚拟环境 ==="
    python3 -m venv venv
fi

# 激活虚拟环境
echo "=== 激活虚拟环境 ==="
source venv/bin/activate

# 安装依赖
echo "=== 安装依赖 ==="
pip install --upgrade pip
pip install -r requirements.txt

# 确保uploads目录存在
echo "=== 创建上传目录 ==="
mkdir -p app/static/uploads
chmod 755 app/static/uploads

# 确保instance目录存在
echo "=== 创建数据库目录 ==="
mkdir -p instance
chmod 755 instance

# 更新数据库
echo "=== 更新数据库 ==="
export FLASK_APP=app.py
flask db upgrade

# 如果数据库为空，初始化
if [ ! -s "instance/food_menu.db" ]; then
    echo "=== 初始化数据库 ==="
    python init_db.py
fi

# 安装systemd服务
if [ -f "/etc/systemd/system/food-menu.service" ]; then
    echo "=== 停止现有服务 ==="
    sudo systemctl stop food-menu
fi

echo "=== 安装systemd服务 ==="
sudo cp food-menu.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable food-menu
sudo systemctl start food-menu

echo "=== 服务已启动 ==="
echo "如需查看服务状态，请运行: sudo systemctl status food-menu"
echo "如需查看服务日志，请运行: sudo journalctl -u food-menu -f"
echo "应用程序现在应该在 http://localhost:5000 上运行"

echo "=== 部署完成 ==="
