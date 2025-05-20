#!/bin/bash
# 部署脚本，用于在服务器上初始化和启动应用

set -e  # 脚本中的任何错误将导致脚本终止

echo "=== 开始部署食品菜单应用 ==="

# 确保在正确的目录中
cd "$(dirname "$0")"

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
pip install -r requirements.txt

# 确保上传目录存在
echo "=== 确保上传目录存在 ==="
mkdir -p app/static/uploads

# 设置文件权限
echo "=== 设置文件权限 ==="
chmod -R 755 .

# 确保数据库目录存在并设置正确权限
echo "=== 设置数据库文件权限 ==="
touch food_menu.db
chmod 666 food_menu.db
current_user=$(whoami)
echo "=== 当前用户: $current_user ==="

# 确保uploads目录存在并有正确权限
echo "=== 设置上传目录权限 ==="
mkdir -p app/static/uploads
chmod 777 app/static/uploads

# 检查SELinux状态（如果存在）
if command -v getenforce > /dev/null; then
    SELINUX_STATUS=$(getenforce)
    echo "=== SELinux状态: $SELINUX_STATUS ==="
    
    if [ "$SELINUX_STATUS" == "Enforcing" ]; then
        echo "注意: SELinux处于强制模式，正在设置适当的上下文..."
        PROJECT_DIR=$(pwd)
        sudo chcon -t httpd_sys_rw_content_t food_menu.db || echo "无法设置SELinux上下文，可能需要手动调整"
        sudo chcon -Rt httpd_sys_rw_content_t app/static/uploads || echo "无法设置uploads目录SELinux上下文"
    fi
fi

# 删除数据库（如果存在）并重新初始化
echo "=== 初始化数据库 ==="
if [ -f "food_menu.db" ]; then
    echo "=== 删除现有数据库 ==="
    rm food_menu.db
fi

echo "=== 运行数据库初始化脚本 ==="
python reinit_db.py

# 再次确保数据库权限正确
echo "=== 最终检查数据库权限 ==="
chmod 666 food_menu.db
ls -la food_menu.db

# 启动应用
echo "=== 启动应用 ==="
echo "以下是启动应用的方法："
echo ""
echo "1. 前台运行（按Ctrl+C停止）:"
echo "   python app.py"
echo ""
echo "2. 后台运行:"
echo "   nohup python app.py > app.log 2>&1 &"
echo ""
echo "3. 使用screen运行（推荐）:"
echo "   screen -S food-menu"
echo "   python app.py"
echo "   (按Ctrl+A然后按D分离screen，使用'screen -r food-menu'重新连接)"
echo ""
echo "=== 部署完成 ==="
