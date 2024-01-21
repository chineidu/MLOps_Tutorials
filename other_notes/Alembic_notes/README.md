# Alembic

- [Docs](https://alembic.sqlalchemy.org/en/latest/)
- [Blog Tutorial (**RECOMMENDED**)](https://learnbatta.com/blog/getting-started-with-alembic/#why-alembic)
- [Video Tutorial (**RECOMMENDED**)](https://www.youtube.com/watch?v=N9y9QkBM-Aw&ab_channel=AnjaneyuluBatta)

## Table of Content

- [Alembic](#alembic)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
    - [Alembic Commands](#alembic-commands)
  - [Creating an Environment](#creating-an-environment)
  - [Alembic Config](#alembic-config)
    - [Adjust SQLAlchemy URL](#adjust-sqlalchemy-url)
  - [Create Revison](#create-revison)
    - [Create First Revision](#create-first-revision)
  - [Operations](#operations)
    - [Create Table (Manually)](#create-table-manually)
    - [Drop Table](#drop-table)
    - [Create Table (Automatically)](#create-table-automatically)

## Installation

```sh
# Virtual ENVs are created in the project directory.
poetry config virtualenvs.in-project true

poetry add alembic
# pip install alembic

```

### Alembic Commands

```sh
alembic -h
```

## Creating an Environment

```sh
alembic init [any_name]

# e.g.
# The init command generates a migrations directory called alembic:
alembic init alembic
```

## Alembic Config

### Adjust SQLAlchemy URL

- Open `alembic.ini` config file.
- If your dialect is Postgres, update the variable `sqlalchemy.url`

```ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s/%(DB_NAME)s
```

- Add the env variables to the `env.py` file.

```py
# Allow interpolation vars to alembic.ini from the host env
section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.environ.get("DB_USER"))
config.set_section_option(section, "DB_PASSWORD", os.environ.get("DB_PASSWORD"))
config.set_section_option(section, "DB_HOST", os.environ.get("DB_HOST"))
config.set_section_option(section, "DB_NAME", os.environ.get("DB_NAME"))
```

## Create Revison

### Create First Revision

- This is used to perform an operation and add a commit message.

```sh
alembic revision -m "your message"

# Create revision
alembic revision -m "create user table"
```

## Operations

### [Create Table (Manually)](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.create_table)

- Upgrade

```py
# current revision file create_user_table.py
from sqlalchemy import INTEGER, VARCHAR, Column, func, TIMESTAMP
from alembic import op


def upgrade() -> None:
    op.create_table(
    "user",
    Column("id", INTEGER, primary_key=True),
    Column("name", VARCHAR(50), nullable=False),
    Column("description", VARCHAR(200)),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
  )
```

- Usage

```sh
# Help
alembic upgrade -h

# Display the generated SQL command/query
alembic upgrade head --sql

# Upgrade to (apply) a new migration
alembic upgrade head
```

### Drop Table

- Downgrade

```py
def downgrade() -> None:
    """This is used to drop a table."""
    op.drop_table(table_name)
```

```sh
alembic downgrade revision_identifier

# e.g. revert to the last migration/operation
alembic downgrade -1
```

### Create Table (Automatically)

```py
# env.py file

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context  # type: ignore

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# NEW!: Allow interpolation vars to alembic.ini from the host env
section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.getenv("DB_USER"))
config.set_section_option(section, "DB_PASSWORD", os.getenv("DB_PASSWORD"))
config.set_section_option(section, "DB_HOST", os.getenv("DB_HOST"))
config.set_section_option(section, "DB_NAME", os.getenv("DB_NAME"))


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from e_commerce_app import models  # NEW!

target_metadata = models.Base.metadata  # NEW!

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    pass

# ==== Other code block ====
```

- Usage

```sh
# Upgrade to (apply) a new migration automatically from the models
alembic revision --autogenerate -m "New Migration"
alembic upgrade head
```
