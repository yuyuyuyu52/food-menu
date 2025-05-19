from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
import sys

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入您的模型
from app import create_app, db
from app.models import Category, Dish

# 获取alembic配置
config = context.config

# 解析配置文件中的section
fileConfig(config.config_file_name)

# 创建Flask应用实例
app = create_app()

# 设置Alembic使用与Flask相同的数据库URI
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# 获取MetaData对象
target_metadata = db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
