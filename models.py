from datetime import datetime

from sqlalchemy import ForeignKey, Table, Column, Integer, PrimaryKeyConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

students_subjects = Table(
    "students_subjects",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("subject_id", Integer, ForeignKey("subjects.id")),
    PrimaryKeyConstraint("student_id", "subject_id"),
)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=func.now())
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=students_subjects, back_populates="students"
    )

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=func.now())

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    students: Mapped[list["Student"]] = relationship(
        secondary=students_subjects, back_populates="subjects"
    )

class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(nullable=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    created: Mapped[datetime] = mapped_column(default=func.now())
