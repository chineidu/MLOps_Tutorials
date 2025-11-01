"""
CRUD operations for managing database entities.
It uses SQLAlchemy ORM v2.xx style queries for efficiency and high performance.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session, selectinload

from .models import ClassProfile, Course, Enrollment, Student


class ClassProfileEnum(str, Enum):
    SCIENCE = "science"
    ARTS = "arts"
    COMMERCIAL = "commercial"


class StudentSchema(BaseModel):
    id: int | None = None
    matric_no: str
    firstname: str
    lastname: str
    age: int
    registered_at: str = Field(default_factory=lambda _: datetime.now().isoformat())
    class_profile: ClassProfileEnum | None = None
    courses: list["CourseSchema"] = Field(default_factory=list)


class CourseSchema(BaseModel):
    id: int | None = None
    name: "CourseNameEnum"
    units: int = Field(ge=1, le=3)
    registered_at: str = Field(default_factory=lambda _: datetime.now().isoformat())
    students: list[StudentSchema] = Field(default_factory=list)


class EnrollmentSchema(BaseModel):
    id: int | None = None
    matric_no: str
    course_id: int
    grade: float | None = None
    registered_at: str = Field(default_factory=lambda _: datetime.now().isoformat())
    student: StudentSchema | None = None
    course: CourseSchema | None = None


class ClassProfileSchema(BaseModel):
    id: int | None = None
    name: str
    profile: ClassProfileEnum | str
    registered_at: str = Field(default_factory=lambda _: datetime.now().isoformat())


class CourseNameEnum(str, Enum):
    ENGLISH_LANGUAGE = "english language"
    MATHEMATICS = "mathematics"
    CIVIC_EDUCATION = "civic education"
    BIOLOGY = "biology"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    LITERATURE_IN_ENGLISH = "literature in english"
    GOVERNMENT = "government"
    ECONOMICS = "economics"
    COMMERCE = "commerce"


# =========================================================
# ==================== CRUD Operations ====================
# =========================================================
def get_class_profile(db: Session, name: str, profile: ClassProfileEnum | str) -> ClassProfile:
    """Get class profile by name."""
    stmt = (
        select(ClassProfile)
        # Select the list of students
        .options(selectinload(ClassProfile.students))
        .where(ClassProfile.name == name, ClassProfile.profile == profile)
    )
    return db.scalar(stmt)


def get_course_name(db: Session, name: CourseNameEnum | str) -> Course:
    """Get course by name."""
    return db.scalar(select(Course).where(Course.name == name))


def get_course_by_id(db: Session, course_id: int) -> Course:
    """Get course by ID."""
    return db.scalar(select(Course).where(Course.id == course_id))


def get_student_by_matric_no(db: Session, matric_no: str) -> Student:
    """Get student by matriculation number."""
    return db.scalar(select(Student).where(Student.matric_no == matric_no))


def get_student_by_id(db: Session, student_id: int) -> Student:
    """Get student by ID."""
    return db.scalar(select(Student).where(Student.id == student_id))


def get_enrollment_by_matric_no_and_course_id(db: Session, matric_no: str, course_id: int) -> Enrollment:
    """Get enrollment by matric_no and course ID."""
    stmt = select(Enrollment).where(Enrollment.matric_no == matric_no, Enrollment.course_id == course_id)
    return db.scalar(stmt)


def get_grades_for_course(db: Session, course_id: int) -> list[Enrollment]:
    """Get all enrollments with grades for a course."""
    stmt = select(Enrollment).where(Enrollment.course_id == course_id)
    return list(db.scalars(stmt).all())


def get_grades_for_student(db: Session, matric_no: str) -> list[Enrollment]:
    """Get all enrollments with grades for a student."""
    stmt = select(Enrollment).where(Enrollment.matric_no == matric_no)
    return list(db.scalars(stmt).all())


def create_student(db: Session, student: StudentSchema) -> Student:
    """Create a new student in the database."""
    try:
        # Check if student already exists
        existing_student = get_student_by_matric_no(db=db, matric_no=student.matric_no)
        if existing_student:
            raise ValueError("Student with the same firstname, lastname and matriculation number already exists.")
        stmt = insert(Student).values(student.model_dump(exclude={"courses", "class_profile"})).returning(Student)
        db_student = db.scalars(stmt).one()
        db.commit()

        return db_student

    except Exception as e:
        db.rollback()
        raise e


def create_class_profile(db: Session, class_profile: ClassProfileSchema) -> ClassProfile:
    """Create a new class profile in the database."""
    try:
        if not get_class_profile(db, name=class_profile.name, profile=class_profile.profile):
            stmt = insert(ClassProfile).values(class_profile.model_dump()).returning(ClassProfile)
            db_class_profile = db.scalar(stmt)
            db.commit()
            return db_class_profile

    except Exception as e:
        db.rollback()
        raise e

    raise ValueError("Class Profile with the same name already exists.")


def create_course_by_name(db: Session, course: CourseSchema) -> Course:
    """Create a new course in the database."""
    try:
        if not get_course_name(db, name=course.name):
            stmt = insert(Course).values(course.model_dump(exclude={"students"})).returning(Course)
            db_course = db.scalar(stmt)
            db.commit()
            return db_course

    except Exception as e:
        db.rollback()
        raise e

    raise ValueError("Course with the same name already exists.")


def enroll_student_into_course(db: Session, enrollment: EnrollmentSchema) -> Enrollment:
    """Enroll an existing student into an existing course."""
    try:
        student = get_student_by_matric_no(db, enrollment.matric_no)
        course = get_course_by_id(db, enrollment.course_id)
        if not student or not course:
            raise ValueError("not found")

        existing = get_enrollment_by_matric_no_and_course_id(
            db=db, matric_no=enrollment.matric_no, course_id=enrollment.course_id
        )
        if existing:
            return existing

        stmt = insert(Enrollment).values(enrollment.model_dump(exclude={"id", "student", "course"})).returning(Enrollment)
        db_enrollment = db.scalar(stmt)
        db.commit()
        return db_enrollment

    except Exception as e:
        db.rollback()
        raise e


def unenroll_student_from_course(db: Session, course_id: int, matric_no: str) -> Course:
    """Remove a student from a course's student list.

    If the student is enrolled, remove them and commit. Returns the Course.
    """
    try:
        student = get_student_by_matric_no(db=db, matric_no=matric_no)
        if not student:
            raise ValueError("Student not found")

        course = get_course_by_id(db=db, course_id=course_id)
        if not course:
            raise ValueError("Course not found")

        # Delete the enrollment record
        delete_stmt = delete(Enrollment).where(Enrollment.matric_no == student.matric_no, Enrollment.course_id == course_id)
        _ = db.scalar(delete_stmt)
        db.commit()

        return course

    except Exception as e:
        db.rollback()
        raise e


def enroll_class_profile(db: Session, class_profile: ClassProfileSchema, matric_no: str) -> ClassProfile:
    """Enroll an existing student into an existing class profile."""
    try:
        cp = get_class_profile(db=db, name=class_profile.name, profile=class_profile.profile)
        if not cp:
            raise ValueError("Class Profile not found")

        student = get_student_by_matric_no(db=db, matric_no=matric_no)
        if not student:
            raise ValueError("Student not found")

        # Verify that the student has not been enrolled
        if student not in cp.students:
            cp.students.append(student)
        db.commit()
        db.refresh(cp)

        return cp

    except Exception as e:
        db.rollback()
        raise e


def unenroll_class_profile(db: Session, class_profile: ClassProfileSchema, matric_no: str) -> ClassProfile:
    """Remove a student from a class profile's student list.

    If the student is enrolled, remove them and commit. Returns the ClassProfile.
    """
    try:
        cp = get_class_profile(db=db, name=class_profile.name, profile=class_profile.profile)
        if not cp:
            raise ValueError("Class Profile not found")

        student = get_student_by_matric_no(db=db, matric_no=matric_no)
        if not student:
            raise ValueError("Student not found")

        if student in cp.students:
            cp.students.remove(student)
            db.commit()
            db.refresh(cp)

        return cp

    except Exception as e:
        db.rollback()
        raise e


def set_grade_for_enrollment(db: Session, matric_no: str, course_id: int, grade: float) -> Enrollment:
    """Set or update the grade for a student's enrollment in a course."""
    try:
        enrollment = get_enrollment_by_matric_no_and_course_id(db, matric_no=matric_no, course_id=course_id)
        if not enrollment:
            raise ValueError("Enrollment not found")
        enrollment.grade = grade
        db.commit()
        db.refresh(enrollment)
        return enrollment

    except Exception as e:
        db.rollback()
        raise e
