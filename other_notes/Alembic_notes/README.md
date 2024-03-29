# Alembic

- [Docs](https://alembic.sqlalchemy.org/en/latest/)
- [Blog Tutorial (**RECOMMENDED**)](https://learnbatta.com/blog/getting-started-with-alembic/#why-alembic)
- [Video Tutorial (**RECOMMENDED**)](https://www.youtube.com/watch?v=N9y9QkBM-Aw&ab_channel=AnjaneyuluBatta)

## Table of Content

- [Alembic](#alembic)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
    - [Alembic Commands](#alembic-commands)
  - [Creating A Project](#creating-a-project)
  - [Alembic Config (Set the `sqlalchemy.url`)](#alembic-config-set-the-sqlalchemyurl)
    - [Method 1](#method-1)
    - [Method 2 (Preferred)](#method-2-preferred)
  - [Create Revison](#create-revison)
    - [Create First Revision](#create-first-revision)
  - [Operations](#operations)
    - [Create Table (Manually)](#create-table-manually)
    - [Drop Table](#drop-table)
    - [Create Table (Automatically)](#create-table-automatically)
  - [Check History](#check-history)
    - [Apply A Specified Revision](#apply-a-specified-revision)
    - [Current Revision](#current-revision)
    - [Rollback Revision](#rollback-revision)

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

## Creating A Project

```sh
alembic init [any_name]

# e.g.
# The init command generates a migrations directory called alembic:
alembic init alembic
```

## Alembic Config (Set the `sqlalchemy.url`)

### Method 1

1.) Update the variable `sqlalchemy.url` in the `alembic.ini` config file like so:

```ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s/%(DB_NAME)s
```

2.) Add the env variables to the `env.py` file.

```py
# Allow interpolation vars to alembic.ini from the host env
section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.environ.get("DB_USER"))
config.set_section_option(section, "DB_PASSWORD", os.environ.get("DB_PASSWORD"))
config.set_section_option(section, "DB_HOST", os.environ.get("DB_HOST"))
config.set_section_option(section, "DB_NAME", os.environ.get("DB_NAME"))
```

### Method 2 (Preferred)

1.) Update the `alembic.ini` config file by setting the variable `sqlalchemy.url` to an empty value.

```ini
sqlalchemy.url =
```

2.) Adjust the `env.py` file.

```py
# env.py


SQLALCHEMY_DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Set the url
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)   # NEW!

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

- `File 1`

```py
from datetime import datetime
from typing import Any, Literal

from sqlalchemy import DateTime, ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

# ===== Other imports =====


class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__: str = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    billing_address: Mapped[str] = mapped_column(String(255), nullable=True)
    shipping_address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)

    order: Mapped["Orders"] = relationship(back_populates="customers")

    def __repr__(self) -> str:
        return (
            f"({self.__class__.__name__}(id={self.id!r}, name={self.name!r}, email={self.email!r}, "
            f"shipping_address={self.shipping_address!r})"
        )


# ===== Other code block =====

```

- `File 2`

```py
# env.py file

from logging.config import fileConfig

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context  # type: ignore
import models  # NEW!

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", models.SQLALCHEMY_DATABASE_URL)   # NEW!

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# Create tables  NEW!
target_metadata = models.Base.metadata

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

## Check History

- This displays all the committed revisions.

```sh
alembic history
```

### Apply A Specified Revision

```sh
alembic upgrade <revison_hash>

# e.g.
alembic upgrade 54954a5a54a5
```

### Current Revision

```sh
alembic current
```

### Rollback Revision

```sh
alembic downgrade <revision>

# e.g.
# last revision
alembic downgrade -1

# specific revision
alembic downgrade 38954a5u64a5
```
