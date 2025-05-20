# 食品菜单应用 - 服务器部署全指南

这个指南将帮助您在服务器上完整部署食品菜单应用程序，包括解决常见问题和设置自动启动服务。

## 目录

1. [基本部署](#基本部署)
2. [数据库问题解决](#数据库问题解决)
3. [服务器配置](#服务器配置)
4. [作为系统服务运行](#作为系统服务运行)
5. [Nginx/Apache配置](#nginx或apache配置)
6. [故障排查](#故障排查)

## 基本部署

### 步骤1: 准备环境

```bash
# 安装必要的包
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# 克隆仓库（如果从Git部署）
git clone <仓库URL> food-menu
cd food-menu

# 或者上传项目文件到服务器
```

### 步骤2: 运行部署脚本

```bash
# 添加执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 步骤3: 启动应用

```bash
# 使用screen（推荐）
screen -S food-menu
source venv/bin/activate
python app.py

# 按Ctrl+A然后按D分离screen会话
```

## 数据库问题解决

如果遇到数据库权限错误，可以使用全面修复脚本：

```bash
# 添加执行权限
chmod +x fix_all_db_issues.sh

# 运行修复脚本
./fix_all_db_issues.sh
```

### 常见数据库问题及解决方案

#### 1. 无法打开数据库文件

错误信息: `sqlite3.OperationalError: unable to open database file`

解决方案:
- 检查文件权限: `chmod 666 food_menu.db`
- 检查目录权限: `chmod 755 .`
- 确保当前用户有写入权限

#### 2. 目录不可写

错误信息: `PermissionError: [Errno 13] Permission denied`

解决方案:
- 设置正确的文件所有者: `sudo chown -R <your_user>:<your_group> .`
- 确保上传目录可写: `chmod 777 app/static/uploads`

#### 3. SELinux限制

如果服务器运行SELinux，它可能会阻止应用访问文件。

解决方案:
```bash
# 查看SELinux状态
getenforce

# 如果是Enforcing，设置适当的上下文
sudo chcon -t httpd_sys_rw_content_t food_menu.db
sudo chcon -Rt httpd_sys_rw_content_t app/static/uploads
```

## 服务器配置

### 端口配置

应用默认在5000端口运行。确保防火墙允许此端口：

```bash
# 对于UFW防火墙
sudo ufw allow 5000/tcp

# 对于iptables
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables-save
```

## 作为系统服务运行

为了使应用在服务器重启后自动启动，可以将其设置为系统服务：

1. 编辑food-menu.service文件，修改路径：
   ```bash
   nano food-menu.service
   # 将所有的 /path/to/food-menu 替换为实际路径
   ```

2. 安装服务：
   ```bash
   sudo cp food-menu.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable food-menu
   sudo systemctl start food-menu
   ```

3. 检查服务状态：
   ```bash
   sudo systemctl status food-menu
   ```

## Nginx或Apache配置

### Nginx配置（推荐）

1. 安装Nginx：
   ```bash
   sudo apt install nginx
   ```

2. 创建配置文件：
   ```bash
   sudo nano /etc/nginx/sites-available/food-menu
   ```

3. 添加以下配置：
   ```
   server {
       listen 80;
       server_name your_domain.com; # 或服务器IP

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /path/to/food-menu/app/static;
       }
   }
   ```

4. 启用站点：
   ```bash
   sudo ln -s /etc/nginx/sites-available/food-menu /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 故障排查

### 检查应用日志

如果应用作为服务运行：
```bash
sudo journalctl -u food-menu -f
```

如果使用nohup运行：
```bash
tail -f app.log
```

### 检查数据库

```bash
# 检查数据库文件权限
ls -la food_menu.db

# 测试数据库连接
sqlite3 food_menu.db .tables
```

### 检查服务器资源

```bash
# 检查磁盘空间
df -h

# 检查内存使用
free -m

# 检查运行中的进程
ps aux | grep python
```

### 检查网络连接

```bash
# 检查端口是否开放
sudo lsof -i :5000

# 测试连接
curl http://localhost:5000
```
