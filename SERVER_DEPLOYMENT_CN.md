# 服务器部署指南

## 常见问题解决方案

### 数据库访问错误

如果遇到 `sqlite3.OperationalError: unable to open database file` 错误，可能是以下原因导致的：

1. **数据库文件权限问题**
2. **路径错误**
3. **目录不存在**

### 解决步骤

1. **运行修复脚本**

   ```bash
   # 进入项目目录
   cd ~/food-menu
   
   # 运行修复脚本
   ./fix_db_server.sh
   ```

2. **手动检查文件权限**

   ```bash
   # 检查数据库文件权限
   ls -la food_menu.db
   
   # 如果数据库文件不存在或权限不正确，运行:
   touch food_menu.db
   chmod 666 food_menu.db
   ```

3. **重新初始化数据库**

   ```bash
   # 激活虚拟环境
   source venv/bin/activate
   
   # 运行初始化脚本
   python reinit_db.py
   ```

4. **确保uploads目录存在并有正确权限**

   ```bash
   mkdir -p app/static/uploads
   chmod 777 app/static/uploads
   ```

## 启动应用

1. **直接启动（前台）**

   ```bash
   source venv/bin/activate
   python app.py
   ```

2. **后台启动**

   ```bash
   source venv/bin/activate
   nohup python app.py > app.log 2>&1 &
   ```

3. **使用Screen后台启动（推荐）**

   ```bash
   # 安装screen（如果未安装）
   sudo apt install screen -y
   
   # 创建新的screen会话
   screen -S food-menu
   
   # 激活环境并启动
   source venv/bin/activate
   python app.py
   
   # 按Ctrl+A然后按D分离会话（应用将在后台运行）
   # 重新连接到会话：screen -r food-menu
   ```

## 故障排查

1. **查看应用日志**

   ```bash
   # 如果使用nohup启动
   tail -f app.log
   ```

2. **检查进程是否运行**

   ```bash
   ps aux | grep "python app.py"
   ```

3. **检查端口是否被占用**

   ```bash
   sudo lsof -i :5000
   ```

4. **设置防火墙允许访问5000端口**

   ```bash
   sudo ufw allow 5000/tcp
   ```
