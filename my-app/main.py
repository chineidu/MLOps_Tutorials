import contextlib
import os
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator, Generic, Optional, TypeVar

from rich.console import Console
from typeguard import typechecked

console = Console()
T = TypeVar("T")

DB_PATH: Path = Path(os.getenv("DB_PATH", "story.db"))


@dataclass
class StorySchema:
    """Data model for creating posts."""

    title: str
    content: str
    tags: Optional[str] = None
    id: Optional[int] = None


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
    def get(self, id: int) -> Optional[StorySchema]:  # type: ignore
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
    def get_all(self) -> Optional[list[StorySchema]]:  # type: ignore
        f"""This is used to fetch all the `stories` from the story table."""
        query: str = f"SELECT id, title, content, tags FROM {self.TABLE_NAME};"
        with self.connect() as cursor:
            cursor.execute(query)
            result: list[StorySchema] = [
                self.__get_result(data=story) for story in cursor.fetchall()
            ]

            return result

    @typechecked
    def add(self, **kwargs) -> Optional[StorySchema]:  # type: ignore
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
    story = StoryRepository(db_path=DB_PATH)
    # story.add(
    #     title="AI Dominance",
    #     content="The battle to become the dominant force in AI is on.",
    #     tags="#AI, #GenAI, #DeepLearning",
    # )

    # story.add(
    #     title="Virgin Mary",
    #     content="Virgin Mary is the mother of our Lord Jesus Christ.",
    #     tags="#Catholic, #Christian, #Jesus",
    # )

    # story.add(
    #     title="Barlays Premier League",
    #     content=(
    #         "Liverpool will be taking on Chelsea at Anfield today. "
    #         "It should be a great game."
    #     ),
    #     tags="#LFC, #CFC, #EPL",
    # )

    # story.delete(id=20)

    console.print(story.get_all())
