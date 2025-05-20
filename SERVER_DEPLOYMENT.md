# 服务器部署问题排查指南

## 数据库访问错误解决方案

如果您在服务器上遇到 `sqlite3.OperationalError: unable to open database file` 错误，请按照以下步骤解决：

1. 运行修复数据库权限的脚本：

```bash
chmod +x fix_db_permissions.sh
./fix_db_permissions.sh
```

2. 确保应用目录和数据库文件的用户和组设置正确：

```bash
# 如果使用www-data运行应用（Apache/Nginx默认用户）
sudo chown -R www-data:www-data /path/to/food-menu
sudo chmod 755 /path/to/food-menu
sudo chmod 666 /path/to/food-menu/food_menu.db
```

3. 如果以上步骤不起作用，请检查SELinux或AppArmor是否限制了文件访问：

```bash
# 在RedHat/CentOS系统上
sudo setenforce 0  # 临时禁用SELinux

# 在Ubuntu系统上
sudo aa-complain /etc/apparmor.d/*  # 将AppArmor设置为记录而不是阻止
```

## 部署步骤完整指南

1. 在服务器上克隆代码仓库：

```bash
git clone https://github.com/your-username/food-menu.git
cd food-menu
```

2. 运行部署脚本：

```bash
chmod +x deploy.sh
./deploy.sh
```

3. 初始化数据库：

```bash
source venv/bin/activate
python reinit_db.py
```

4. 启动应用：

```bash
# 开发环境
python run.py

# 生产环境（使用Gunicorn）
gunicorn -w 4 "run:app" -b 0.0.0.0:5000
```

## 使用systemd进行服务管理（推荐）

创建一个systemd服务文件来管理应用：

1. 创建服务文件：

```bash
sudo nano /etc/systemd/system/food-menu.service
```

2. 添加以下内容（替换路径为实际路径）：

```
[Unit]
Description=Food Menu Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/food-menu
ExecStart=/path/to/food-menu/venv/bin/gunicorn -w 4 "run:app" -b 0.0.0.0:5000
Restart=always
Environment="PATH=/path/to/food-menu/venv/bin"
Environment="PYTHONPATH=/path/to/food-menu"

[Install]
WantedBy=multi-user.target
```

3. 启动并启用服务：

```bash
sudo systemctl start food-menu
sudo systemctl enable food-menu
```

4. 查看服务状态：

```bash
sudo systemctl status food-menu
```

## 查看应用日志

```bash
# 如果使用systemd
sudo journalctl -u food-menu

# 如果使用直接运行
tail -f app.log
```
