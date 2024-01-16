# SQL ORM Tutorials

- `Expression Construct` is the modern API.

## Table of Content

- [SQL ORM Tutorials](#sql-orm-tutorials)
  - [Table of Content](#table-of-content)
  - [SQLAlchemy](#sqlalchemy)
    - [Setting Up MetaData With Table Objects](#setting-up-metadata-with-table-objects)
    - [Declarative Approach](#declarative-approach)
    - [Insert Data](#insert-data)
      - [Declarative Insert Approach](#declarative-insert-approach)
      - [Insert 2 (Expression Construct)](#insert-2-expression-construct)
    - [Select Statement](#select-statement)
    - [Select Statement (Expression Construct)](#select-statement-expression-construct)
    - [Update a specific row](#update-a-specific-row)
    - [Update a specific Row (Expression Construct)](#update-a-specific-row-expression-construct)
    - [Delete a specific row](#delete-a-specific-row)
    - [Delete a specific row (Expression Construct)](#delete-a-specific-row-expression-construct)
  - [Bulk (Expression Construct)](#bulk-expression-construct)
    - [Bulk Insert](#bulk-insert)
      - [Clossing A Session](#clossing-a-session)
    - [Drop Table](#drop-table)

## SQLAlchemy

- [Engine (docs)](https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

console= Console()

# Sqlite dialect
path: str = "sqlite+pysqlite:///:memory:"
engine = create_engine(path, echo=True)

# Connetion object
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    console.print(result.all())
    conn.commit()

# Session object
with Session(engine) as session:
    result = session.execute(text("select 'hello Neidu'"))
    console.print(result.all())
    session.commit()
```

### Setting Up MetaData With Table Objects

```python
from sqlalchemy import MetaData, Table, Column, Integer, String


metadata_obj = MetaData()

# name, metadata
user_table: Table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(300))
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(1_000), nullable=False),
)

metadata_obj.create_all(engine)
```

### Declarative Approach

```python
from typing import Optional
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship

from rich.console import Console


console = Console()

# Sqlite dialect
path: str = "sqlite+pysqlite:///:memory:"
engine = create_engine(path, echo=True)
session = Session(engine)


### Declarative Approach
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"(User(id={self.id!r}, name={self.name!r}, "
            f"fullname={self.fullname!r}, addresses={self.addresses!r})"
        )


class Address(Base):
    __tablename__: str = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# Create tables
Base.metadata.create_all(engine)

```

### Insert Data

- [Table Approach](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html#tutorial-core-insert)

#### Declarative Insert Approach

```python
neidu: User = User(name="neidu", fullname="Chinedu Emmanuel")
sandy: User = User(name="sandy", fullname="Sandy Kenbrigs")
console.print(neidu)

session.add(neidu)
session.add(sandy)
session.commit()
```

#### Insert 2 (Expression Construct)

```python
from sqlalchemy import insert


stmt = insert(User).values(name="jude", fullname="Jude Bags")
session.execute(stmt)
session.commit()
```

### Select Statement

```python
# Select a specific row(s)
result = session.query(User).filter(User.name == "neidu").all()
console.print(f"result1: {result}")

# OR
result = session.get(User, 1)
console.print(f"result2: {result}")
```

### Select Statement (Expression Construct)

```python
from sqlalchemy import select


stmt = select(User).where(User.name == "jude")
# stmt = select(User).filter_by(name="jude", fullname="Jude Bags")
result = session.execute(stmt).scalar_one()

# Select all
result = session.execute(select(Users)).scalars().all()
```

### Update a specific row

```python

neidu_name = session.query(User).filter(User.name == "neidu").first()
all_data = session.query(User).all()

# Update
try:
    neidu_name.name = "michael"
    session.commit()
    console.print("User updated successfully!", style="green")

except Exception as err:
    console.print(f"Error updating user: {err}", style="red")
    session.rollback()  # Rollback changes on error
```

### Update a specific Row (Expression Construct)

```python
from sqlalchemy import update


stmt = (
          update(User)
          .where(User.name == "neidu")
          .values(fullname="Don Baba J")
          )

# Update
try:
    session.execute(stmt)
    session.commit()
    console.print("User updated successfully!", style="green")

except Exception as err:
    console.print(f"Error updating user: {err}", style="red")
    session.rollback()  # Rollback changes on error
```

### Delete a specific row

```python
patrick = User(name="pahto", fullname="Patrick Adebayo")
session.add(patrick)

patrick_name = session.query(User).filter(User.name == "pahto").first()

# Delete
try:
    session.delete(patrick_name)
    session.commit()
    console.print("User deleted successfully!", style="green")

except Exception as err:
    console.print(f"Error deleting user: {err}", style="red")
    session.rollback()  # Rollback changes on error
```

### Delete a specific row (Expression Construct)

```python
from sqlalchemy import delete

stmt = delete(User).where(User.name == "pahto")
# stmt = delete(User).filter_by(name="pahto")

# Delete
try:
    session.execute(stmt)
    session.commit()
    console.print("User deleted successfully!", style="green")

except Exception as err:
    console.print(f"Error deleting user: {err}", style="red")
    session.rollback()  # Rollback changes on error
```

## Bulk (Expression Construct)

- [Docs](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete)

### Bulk Insert

```python
new_users: list[dict[str, Any]] = [
    {"name": "spongebob", "fullname": "Spongebob Squarepants"},
    {"name": "sandy", "fullname": "Sandy Cheeks"},
    {"name": "patrick", "fullname": "Patrick Star"},
    {"name": "squidward", "fullname": "Squidward Tentacles"},
    {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
]

# Bulk Insert
try:
    users = session.scalars(insert(User).returning(User), new_users)
    session.commit()
    console.print(users.all())
    console.print("User inserted successfully!", style="green")

except Exception as err:
    console.print(f"Error inserting user: {err}", style="red")
    session.rollback()  # Rollback changes on error
```

#### Clossing A Session

```python
path: str = "sqlite:///./test.db"
engine = create_engine(path, echo=True)
session = Session(engine)

...

session.close()
```

### Drop Table

```python
from sqlalchemy.schema import DropTable


address_table = Address.__table__
session.execute(DropTable(address_table))
session.commit()
```
