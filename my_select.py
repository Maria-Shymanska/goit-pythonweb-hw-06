from models import Student, Teacher, Group, Subject, Grade, students_subjects
from connect import engine, session
from sqlalchemy import Null, func
import random


# 1. 5 student with the highest average grade
def select_1():
    students = (
        session.query(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.round(func.avg(Grade.value), 1).label("avg_grade"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )

    print("5 student with the highest average score:")
    for row in students:
        print(row)


# 2. the student with the highest average grade in particular subject
def select_2(subject_name):
    student = (
        session.query(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.avg(Grade.value).label("avg_grade"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .join(students_subjects, Student.id == students_subjects.c.student_id)
        .join(Subject, students_subjects.c.subject_id == Subject.id)
        .filter(Subject.title == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(1)
        .all()
    )

    print(
        f"Student with the highest score in the subject {subject_name}: {student[0].first_name} {student[0].last_name}"
    )


# 3. Average score in groups in a particular subject
def select_3(subject_name):
    groups = (
        session.query(
            Group.name.label("group_name"),
            func.round(func.avg(Grade.value), 1).label("avg_grade"),
        )
        .join(Student, Group.id == Student.group_id)
        .join(students_subjects, Student.id == students_subjects.c.student_id)
        .join(Subject, students_subjects.c.subject_id == Subject.id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Subject.title == subject_name)
        .group_by(Group.name)
        .all()
    )

    print(f"Average score in groups of {subject_name} subject:")
    for row in groups:
        print(row)


# Середній бал на потоці (по всій таблиці оцінок)
def select_4():
    avg_grade = session.query(
        func.round(func.avg(Grade.value), 1).label("avg_grade")
    ).scalar()
    print(f"Average score on stream (across the scoreboard): {avg_grade}")


# 5. What courses does a particular teacher teach
def select_5(teacher_name):
    subjects = (
        session.query(Subject.title)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.first_name == teacher_name)
        .all()
    )

    print(f"What courses does the teacher teach {teacher_name}:")
    for row in subjects:
        print(row)


# 6. List of students in a specific group
def select_6(group_name):
    students = (
        session.query(Student.first_name, Student.last_name)
        .join(Group, Group.id == Student.group_id)
        .filter(Group.name == group_name)
        .all()
    )

    print(f"List of students in group {group_name}:")
    for row in students:
        print(row)


# 7. Grades of students in a separate group in a particular subject
def select_7(group_name, subject_name):
    students = (
        session.query(Student.first_name, Student.last_name, Grade.value)
        .join(Group, Group.id == Student.group_id)
        .join(students_subjects, students_subjects.c.student_id == Student.id)
        .join(Subject, Subject.id == students_subjects.c.subject_id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Group.name == group_name)
        .filter(Subject.title == subject_name)
        .all()
    )

    print(f"Grades of students in {group_name} the group {subject_name} of the subject:")
    for row in students:
        print(row)


# 8. The average score given by a certain teacher in their subjects
def select_8(teacher_name):
    avg_grade = (
        session.query(func.round(func.avg(Grade.value), 1).label("avg_grade"))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Teacher.first_name == teacher_name)
        .scalar()
    )

    print(
        f"Average score given by {teacher_name} teacher in their subjects: {avg_grade}"
    )


# 9. List of courses taken by a particular student
def select_9(student_name):
    subjects = (
        session.query(Subject.title)
        .join(students_subjects, students_subjects.c.subject_id == Subject.id)
        .join(Student, students_subjects.c.student_id == Student.id)
        .filter(Student.first_name == student_name)
        .all()
    )

    print(f"List of courses attended by {student_name} student:")
    for row in subjects:
        print(row)


# 10. List of courses taught to a particular student by a particular teacher
def select_10(student_name, teacher_name):
    subjects = (
        session.query(Subject.title)
        .join(students_subjects, students_subjects.c.subject_id == Subject.id)
        .join(Student, students_subjects.c.student_id == Student.id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Student.first_name == student_name)
        .filter(Teacher.first_name == teacher_name)
        .all()
    )

    print(f"List of courses that {student_name} student is taught by a {teacher_name} teacher:")
    for row in subjects:
        print(row)


# Tools
def getRandomTeacher():
    teachers = session.query(Teacher.first_name).distinct().all()
    if teachers:
        random_teacher_name = random.choice(teachers)[0]
        return random_teacher_name
    else:
        return Null


def getRandomSubject():
    subject = session.query(Subject.title).distinct().all()
    if subject:
        random_subject = random.choice(subject)[0]
        return random_subject
    else:
        return Null


def getRandomGroup():
    group = session.query(Group.name).distinct().all()
    if group:
        random_group = random.choice(group)[0]
        return random_group
    else:
        return Null


def getRandomStudent():
    student = session.query(Student.first_name).distinct().all()
    if student:
        random_student = random.choice(student)[0]
        return random_student
    else:
        return Null


if __name__ == "__main__":
    with engine.connect() as connection:
        select_1()

        subject_name = getRandomSubject()
        if subject_name:
            select_2(subject_name)
            select_3(subject_name)

        select_4()

        teacher_name = getRandomTeacher()
        if teacher_name:
            select_5(teacher_name)

        group_name = getRandomGroup()
        if group_name:
            select_6(group_name)

        if subject_name and group_name:
            select_7(group_name, subject_name)

        if teacher_name:
            select_8(teacher_name)

        student_name = getRandomStudent()
        if student_name:
            select_9(student_name)

        if student_name and teacher_name:
            select_10(student_name, teacher_name)
