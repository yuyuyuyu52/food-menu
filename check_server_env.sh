#!/bin/bash
# 系统环境检查脚本
# 用于在部署前检查服务器环境是否满足要求

echo "===== 服务器环境检查 ====="

# 1. 检查操作系统
echo "操作系统信息:"
cat /etc/os-release
echo "-------------------"

# 2. 检查Python版本
echo "Python版本:"
python3 --version
echo "-------------------"

# 3. 检查磁盘空间
echo "磁盘空间:"
df -h .
echo "-------------------"

# 4. 检查内存
echo "内存信息:"
free -h
echo "-------------------"

# 5. 检查必要软件包
echo "必要软件包检查:"
MISSING_PKGS=""

# 检查pip
if ! command -v pip3 &> /dev/null; then
    MISSING_PKGS="$MISSING_PKGS python3-pip"
fi

# 检查venv
python3 -c "import venv" 2>/dev/null
if [ $? -ne 0 ]; then
    MISSING_PKGS="$MISSING_PKGS python3-venv"
fi

# 检查sqlite3
if ! command -v sqlite3 &> /dev/null; then
    MISSING_PKGS="$MISSING_PKGS sqlite3"
fi

if [ -n "$MISSING_PKGS" ]; then
    echo "缺少以下软件包: $MISSING_PKGS"
    echo "请使用以下命令安装:"
    echo "sudo apt update && sudo apt install -y $MISSING_PKGS"
else
    echo "所有必要软件包已安装"
fi
echo "-------------------"

# 6. 检查防火墙状态
echo "防火墙状态:"
if command -v ufw &> /dev/null; then
    sudo ufw status
elif command -v firewalld &> /dev/null; then
    sudo firewall-cmd --state
    echo "检查5000端口是否开放:"
    sudo firewall-cmd --list-ports | grep 5000 || echo "5000端口未开放"
else
    echo "未检测到UFW或Firewalld防火墙"
fi
echo "-------------------"

# 7. 检查SELinux状态
echo "SELinux状态:"
if command -v getenforce &> /dev/null; then
    getenforce
else
    echo "SELinux未安装或不可用"
fi
echo "-------------------"

# 8. 检查端口占用
echo "端口5000占用情况:"
if command -v lsof &> /dev/null; then
    sudo lsof -i :5000 || echo "端口5000未被占用"
elif command -v netstat &> /dev/null; then
    sudo netstat -tulpn | grep :5000 || echo "端口5000未被占用"
else
    echo "未安装lsof或netstat，无法检查端口占用"
fi
echo "-------------------"

# 9. 检查Web服务器
echo "Web服务器状态:"
if command -v nginx &> /dev/null; then
    echo "Nginx已安装:"
    nginx -v
    systemctl status nginx | grep Active || echo "Nginx未运行"
elif command -v apache2 &> /dev/null; then
    echo "Apache已安装:"
    apache2 -v
    systemctl status apache2 | grep Active || echo "Apache未运行"
else
    echo "未安装Nginx或Apache"
fi
echo "-------------------"

# 10. 总结报告
echo "===== 环境检查总结 ====="
echo "请确保:"
echo "1. Python 3.6+已安装"
echo "2. 有足够的磁盘空间(至少100MB)"
echo "3. 有足够的内存(至少256MB可用)"
echo "4. 安装了所有必要的软件包"
echo "5. 端口5000未被占用或已在防火墙中开放"
echo "6. 如果使用SELinux，已正确配置访问权限"
echo "======================="
