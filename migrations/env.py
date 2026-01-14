from logging.config import fileConfig
import os

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

from models.base import Base

load_dotenv()

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Load DATABASE_URL
database_url = os.getenv("DATABASE_URL")

if database_url.startswith("postgresql+asyncpg"):
    database_url = database_url.replace("postgresql+asyncpg", "postgresql")

safe_url = database_url.replace("%", "%%")

config.set_main_option("sqlalchemy.url", safe_url)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
