# Python Tutorials

## Table of Content

- [Python Tutorials](#python-tutorials)
  - [Table of Content](#table-of-content)
  - [Class Methods](#class-methods)
  - [Types](#types)
    - [TypeVar](#typevar)
    - [Generic Types](#generic-types)
  - [Repository Design Pattern](#repository-design-pattern)
    - [A Simple Example](#a-simple-example)
  - [Abstract Factory](#abstract-factory)
  - [PyDantic BaseSettings (For Configurations)](#pydantic-basesettings-for-configurations)
  - [Singleton Pattern](#singleton-pattern)

## Class Methods

```py
from typing import TypeVar, Type
from sqlalchemy import select, delete


from rich.console import Console
from typeguard import typechecked


console = Console()

P = TypeVar("P", bound="Product")


class Product:
    base_price: float = 100.0  # class attribute

    @typechecked
    def __init__(self, name: str, discount: float = 0) -> None:
        self.name = name
        if 0 <= discount <= 1:
            self.discount = discount
        else:
            raise ValueError("discount must be between 0 and 1")

    @typechecked
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, discount={self.discount})"

    @typechecked
    @classmethod
    def from_string(cls: Type[P], product_str) -> P:
        """Create the product from a string.
        It uses the format: "name, discount"
        """
        name, discount = product_str.split(",")
        return cls(name, float(discount))

    @typechecked
    @classmethod
    def set_base_price(cls: Type[P], new_price: float) -> None:
        """Change the base price for all the products."""
        cls.base_price = new_price

    @typechecked
    def calculate_price(self) -> float:
        """Calculate the final price using the discount."""
        final_price: float = self.base_price * (1 - self.discount)
        return final_price


Product.set_base_price(120.0)
p1 = Product(name="Airbuds", discount=0.05)
p2 = Product.from_string(product_str="Google Chromecast, 0.035")
console.print(p1, style="green")  # Product(name=Airbuds, discount=0.05)
console.print(p2, style="blue")  # Product(name=Google Chromecast, discount=0.035)

price_1 = p1.calculate_price()
price_2 = p2.calculate_price()

console.print(price_1, style="green")  # 114.0
console.print(price_2, style="blue")  # 115.8
```

## Types

### TypeVar

- They act as placeholders for different types.
- Type variables are only used for type hints and annotations, not for runtime type checking.

```py
from typing import TypeVar

T = TypeVar("T")

def swap(x: T, y: T) -> tuple[T, T]:
    return y, x

# Works with different types:
result1 = swap(10, 20)  # Ints
result2 = swap("hello", "world")  # Strings
```

### Generic Types

- `Generic` itself isn't directly used in type hints or function calls.
- It provides the underlying structure for the generic class.

```py
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    """A class that can be used with different data types."""

    def __init__(self):
        self.items = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

# Create stacks for different types:
int_stack = Stack[int]()  # Stack for integers
str_stack = Stack[str]()  # Stack for strings

```

## Repository Design Pattern

- `Abstracts` `data access` logic from `business` logic, promoting a clean and maintainable architecture.

- Acts as a bridge between application layers and data storage mechanisms.

- Generally, it contains an abstraction of:
  - `Business/Domain logic` implemention like a `User` class.
  - `Generic repository interface` defining data access.
  - An `actual implementation` for data access logic

### A Simple Example

```py
import contextlib
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator, Generic, Optional, TypeVar

from rich.console import Console
from typeguard import typechecked

console = Console()


T = TypeVar("T")

# 1. Business logic!
@dataclass
class StorySchema:
    """Data model for creating posts."""

    title: str
    content: str
    tags: Optional[str] = None
    id: Optional[int] = None


# 2. Generic repository interface!
class Repository(ABC, Generic[T]):
    """This is a base class for interacting with the database."""

    @abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: int, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError

# 3. Actual implementation!
class StoryRepository(Repository[StorySchema]):
    """This class is used for creating a `story` table and manipulating (CRUD) the `story` table.
    It uses a SQLite dialect.
    """

    TABLE_NAME: str = "Story"

    @typechecked
    def __init__(self, db_path: Path = Path("story.db")) -> None:
        self.db_path = db_path
        self.create_table()

    @contextlib.contextmanager
    @typechecked
    def connect(self) -> Generator[sqlite3.Cursor, None, None]:
        """This is used for creating a SQLite connection to the database.

        sqlite3.Cursor: type of values yielded by the generator.
        None: type of values that can be sent to the generator.
        None: return type of the generator.
        """
        with sqlite3.connect(database=self.db_path) as conn:
            try:
                yield conn.cursor()
            except Exception as err:
                console.print(f"[ERROR]: {err}", style="red")

    @typechecked
    def create_table(self) -> None:
        f"""This is used to create the story table."""
        with self.connect() as cursor:
            cursor.execute(
                (
                    f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} "
                    "(id INTEGER PRIMARY KEY, title TEXT, content TEXT, tags TEXT);"
                )
            )
            console.print(f"[INFO]: {self.TABLE_NAME} successfully created!", style="green")

    @typechecked
    def __get_result(self, data: tuple[Any, Any, Any, Any]) -> StorySchema:
        """This is a helper function for creating a StorySchema object."""
        result: StorySchema = StorySchema(id=data[0], title=data[1], content=data[2], tags=data[3])
        return result

    @typechecked
    def get(self, id: int) -> Optional[StorySchema]:
        f"""This is used to fetch a story from the story table."""
        query: str = f"SELECT id, title, content, tags FROM {self.TABLE_NAME} WHERE id = ?;"
        with self.connect() as cursor:
            cursor.execute(query, (id,))
            story = cursor.fetchone()

            if story is None:
                raise ValueError(f"Story with id={id} does not exist!")

            result: StorySchema = self.__get_result(data=story)

            return result

    @typechecked
    def get_all(self) -> Optional[list[StorySchema]]:
        f"""This is used to fetch all the `stories` from the story table."""
        query: str = f"SELECT id, title, content, tags FROM {self.TABLE_NAME};"
        with self.connect() as cursor:
            cursor.execute(query)
            result: list[StorySchema] = [
                self.__get_result(data=story) for story in cursor.fetchall()
            ]

            return result

    @typechecked
    def add(self, **kwargs) -> Optional[StorySchema]:
        if "title" in kwargs and "content" in kwargs and "tags" in kwargs:
            with self.connect() as cursor:
                query: str = (
                    f"INSERT INTO {self.TABLE_NAME} (title, content, tags) VALUES (?, ?, ?);"
                )
                cursor.execute(
                    query,
                    (kwargs.get("title"), kwargs.get("content"), kwargs.get("tags")),
                )
                result: StorySchema = StorySchema(**kwargs)
                return result

        elif "title" in kwargs and "content" in kwargs:
            with self.connect() as cursor:
                query = f"INSERT INTO {self.TABLE_NAME} (title, content) VALUES (?, ?);"
                cursor.execute(query, (kwargs.get("title"), kwargs.get("content")))
                result = StorySchema(**kwargs)
                return result

        else:
            raise ValueError("`title` and `content` cannot be empty!")

    def update(self, id: int, **kwargs: object) -> StorySchema:
        """This is used to update a story."""
        if "title" in kwargs and "content" in kwargs and "tags" in kwargs:
            with self.connect() as cursor:
                query: str = f"UPDATE {self.TABLE_NAME} SET title=?, content=?, tags=? WHERE id=?;"
                cursor.execute(
                    query,
                    (
                        kwargs.get("title"),
                        kwargs.get("content"),
                        kwargs.get("tags"),
                        id,
                    ),
                )
                result: StorySchema = StorySchema(**kwargs)  # type: ignore
                return result

        elif "title" in kwargs and "content" in kwargs:
            with self.connect() as cursor:
                query = f"UPDATE {self.TABLE_NAME} SET title=?, content=? WHERE id=?;"
                cursor.execute(query, (kwargs.get("title"), kwargs.get("content"), id))
                result = StorySchema(**kwargs)  # type: ignore
                return result

        elif "title" in kwargs:
            with self.connect() as cursor:
                query = f"UPDATE {self.TABLE_NAME} SET title=? WHERE id=?;"
                cursor.execute(query, (kwargs.get("title"), id))
                result = StorySchema(**kwargs)  # type: ignore
                return result

        elif "content" in kwargs:
            with self.connect() as cursor:
                query = f"UPDATE {self.TABLE_NAME} SET content=? WHERE id=?;"
                cursor.execute(query, (kwargs.get("content"), id))
                result = StorySchema(**kwargs)  # type: ignore
                return result

        else:
            raise ValueError("You must enter at least of `title` or `content` cannot be empty!")

    @typechecked
    def delete(self, id: int) -> None:
        """This is used to delete a story."""
        with self.connect() as cursor:
            query: str = f"DELETE FROM {self.TABLE_NAME} WHERE id=?;"
            try:
                cursor.execute(query, (id,))
                if cursor.rowcount > 0:
                    console.print("[INFO]: Story successfully deleted!", style="green")
                else:
                    console.print(f"[INFO]: No story found with id={id}", style="green")

            except Exception as err:
                console.print(f"[ERROR]: {err}", style="red")


if __name__ == "__main__":
    story = StoryRepository()
    story.add(
        title="AI Dominance",
        content="The battle to become the dominant for ce in AI is on",
        tags="#AI, #GenAI, #DeepLearning",
    )
    console.print(story.get_all())

```

## Abstract Factory

- The `Abstract Factory Pattern` provides an interface for creating families of related or dependent objects without specifying their creation logic/classes.

```py
from abc import ABC, abstractmethod

# Abstract Product A
class AbstractChair(ABC):
    @abstractmethod
    def sit_on(self):
        raise NotImplementedError

# Concrete Product A1
class ModernChair(AbstractChair):
    def sit_on(self):
        return "Sitting on a modern chair"

# Concrete Product A2
class VictorianChair(AbstractChair):
    def sit_on(self):
        return "Sitting on a Victorian chair"

# Abstract Product B
class AbstractTable(ABC):
    @abstractmethod
    def eat_on(self):
        raise NotImplementedError

# Concrete Product B1
class ModernTable(AbstractTable):
    def eat_on(self):
        return "Eating on a modern table"

# Concrete Product B2
class VictorianTable(AbstractTable):
    def eat_on(self):
        return "Eating on a Victorian table"

# Abstract Factory
class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self) -> AbstractChair:
        raise NotImplementedError

    @abstractmethod
    def create_table(self) -> AbstractTable:
        pass

# Concrete Factory 1
class ModernFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> AbstractChair:
        return ModernChair()

    def create_table(self) -> AbstractTable:
        return ModernTable()

# Concrete Factory 2
class VictorianFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> AbstractChair:
        return VictorianChair()

    def create_table(self) -> AbstractTable:
        return VictorianTable()

# Client Code
def client_code(factory: FurnitureFactory):
    chair = factory.create_chair()
    table = factory.create_table()

    print(chair.sit_on())
    print(table.eat_on())

# Using Modern Furniture Factory
modern_factory = ModernFurnitureFactory()
client_code(modern_factory)

# Using Victorian Furniture Factory
victorian_factory = VictorianFurnitureFactory()
client_code(victorian_factory)

```

## PyDantic BaseSettings (For Configurations)

```.env
# Contents of `.my_env`

name="Neidu"
url="localhost"
```

```py
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

# Load env variables
load_dotenv(dotenv_path=find_dotenv(filename=".my_env"))


class MySettings(BaseSettings):
    name: str  # Optional i.e. MUST be defined as env vars or during init
    url: str  # Optional
    port: int = 5000

    class Config:
        env_file = ".my_env"


# Usage
# Approach 1: Must have loaded variables from an env file called `.my_env`
settings_1 = MySettings()
print(settings_1)


# Approach 2: Manually initialize the config variables
settings_2 = MySettings(name="my app name", url="http://www.myapp.com")
print(settings_2)
```

## Singleton Pattern

- The `Singleton Pattern` ensures that a class has only one instance and provides a global point of access to it.

```py
class MySingleton:
    """A simple implementation of the Singleton Pattern."""
    _instance: "None | MySingleton" = None
    _is_initialized: bool = False

    def __new__(cls, name: str, age: int) -> "MySingleton":
        # If instance is not created, create it
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._name = name
            cls._instance._age = age
        return cls._instance

    def __init__(self, name: str, age: int) -> None:
        # Only initialize if not already initialized
        if not self._is_initialized:
            self._age: int = age
            self._name: str = name
            self._is_initialized = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name}, age={self._age})"

# Usage
my_singleton_1 = MySingleton(name="Mike", age=37)
my_singleton_2 = MySingleton(name="Ada", age=29)

print(my_singleton_1)  # Output: MySingleton(name=Mike, age=37)
print(my_singleton_2)  # Output: MySingleton(name=Mike, age=37)

print(my_singleton_1 == my_singleton_2)  # Output: True
```
