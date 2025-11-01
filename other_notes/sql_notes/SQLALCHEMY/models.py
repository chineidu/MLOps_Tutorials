from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from src.config import app_settings

from .config import DatabasePool, create_logger

logger = create_logger("test_model")


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


# 1 unique student (students table) to 1 unique profile (profiles table) [1 to 1]
# Many to many: 1 student can take multiple courses; and 1 course can be taken by multiple students

# For many <-> many, we need an association (additional) table to accurately track the tables
# Removed: student_courses = Table(...) because it can only be used for simple many-to-many
# relationships without extra data
# student_courses = Table(
#     "student_courses",
#     Base.metadata,
#     Column("student_id", ForeignKey("students.id"), primary_key=True),
#     Column("course_id", ForeignKey("courses.id"), primary_key=True),
# )
# I used `Enrollment` as the association object instead to track: student_id, course_id, grade, registered_at, etc.


class Student(Base):
    __tablename__: str = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    matric_no: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    registered_at: Mapped[str] = mapped_column(DateTime(timezone=True), default=func.now())

    # =========================================================
    # ==================== Relationships ======================
    # =========================================================

    # One to one (i.e. one student -> one class profile). Requires a foreign key!
    # (Because a student can ONLY have one profile)
    profile_id = mapped_column(Integer, ForeignKey("class_profiles.id"))
    class_profile = relationship("ClassProfile", back_populates="students")

    # List of courses taken by the student (convenience viewonly)
    # many students <-> many courses
    courses = relationship("Course", secondary="enrollments", viewonly=True, back_populates="students")
    # List of enrollments for this student
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(matric_no={self.matric_no}, registered_at={self.registered_at})"


class Course(Base):
    __tablename__: str = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    units: Mapped[int] = mapped_column(Integer, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    # =========================================================
    # ==================== Relationships ======================
    # =========================================================

    # Many to many (i.e. many students <-> many courses) convenience viewonly
    students = relationship("Student", secondary="enrollments", viewonly=True, back_populates="courses")
    # List of enrollments for this course
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, units={self.units})"


class Enrollment(Base):
    """
    Association table for many-to-many relationship between Student and Course.
    Also stores additional data like grade and registration date.
    """

    __tablename__: str = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True)
    matric_no: Mapped[str] = mapped_column(ForeignKey("students.matric_no"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    grade: Mapped[float] = mapped_column(nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    # =========================================================
    # ==================== Relationships ======================
    # =========================================================

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    # Ensure ONLY a single enrollment per student per course
    __table_args__: tuple[UniqueConstraint] = (UniqueConstraint("matric_no", "course_id", name="uix_student_course"),)


class ClassProfile(Base):
    __tablename__: str = "class_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    profile: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)  # science, art or commercial
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    # =========================================================
    # ==================== Relationships ======================
    # =========================================================

    # One to many (i.e. one class_profile -> many students) Doesn't require foreign key!
    # List of students with a given profile
    # back_populates must match the attribute name on Student ('class_profile')
    students = relationship("Student", back_populates="class_profile")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, profile={self.profile}, registered_at={self.registered_at})"


# =========================================================
# ==================== Utilities ==========================
# =========================================================
# Global pool instance
_db_pool: DatabasePool | None = None


def get_db_pool() -> DatabasePool:
    """Get or create the global database pool."""
    global _db_pool
    if _db_pool is None:
        _db_pool = DatabasePool(app_settings.database_url_2)
    return _db_pool


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session context manager.

    Use this for manual session management with 'with' statements.

    Yields
    ------
    Session
        A database session
    """
    db_pool = get_db_pool()
    with db_pool.get_session() as session:
        yield session


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions.

    This is a generator function that FastAPI will handle automatically.
    Use this with Depends() in your route handlers.

    Yields
    ------
    Session
        A database session that will be automatically closed after the request
    """
    db_pool = get_db_pool()
    with db_pool.get_session() as session:
        try:
            yield session
        finally:
            # Session cleanup is handled by the context manager
            pass


def init_db() -> None:
    """This function is used to create the tables in the database.
    It should be called once when the application starts."""
    db_pool = get_db_pool()
    # Create all tables in the database
    Base.metadata.create_all(db_pool.engine)
    logger.info("Database initialized")


if __name__ == "__main__":
    init_db()
