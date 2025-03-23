from faker import Faker
from faker import Faker
import random
from datetime import datetime, timedelta
from models import Base, Student, Teacher, Group, Subject, Grade, students_subjects
from connect import engine, Base, session

fake = Faker()

Base.metadata.create_all(engine)

session.query(Grade).delete()
session.query(students_subjects).delete()
session.query(Student).delete()
session.query(Subject).delete()
session.query(Teacher).delete()
session.query(Group).delete()
session.commit()

groups = [
    Group(name="Group A"),
    Group(name="Group B"),
    Group(name="Group C")
]
session.add_all(groups)
session.commit()

teachers = []
for _ in range(5):
    teacher = Teacher(
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    teachers.append(teacher)
session.add_all(teachers)
session.commit()

subjects = [
    Subject(title="Mathematics", teacher_id=random.choice(teachers).id),
    Subject(title="Physics", teacher_id=random.choice(teachers).id),
    Subject(title="Chemistry", teacher_id=random.choice(teachers).id),
    Subject(title="Biology", teacher_id=random.choice(teachers).id),
    Subject(title="History", teacher_id=random.choice(teachers).id),
    Subject(title="Literature", teacher_id=random.choice(teachers).id)
]
session.add_all(subjects)
session.commit()

students = []
for _ in range(40):
    student = Student(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        group_id=random.choice(groups).id
    )
    student_subjects = random.sample(subjects, k=random.randint(3, 6))
    student.subjects = student_subjects
    students.append(student)
session.add_all(students)
session.commit()

current_date = datetime.now()
for student in students:
    for _ in range(random.randint(15, 20)):
        subject = random.choice(student.subjects)
        random_days = random.randint(0, 365)
        grade_date = current_date - timedelta(days=random_days)
        grade = Grade(
            value=random.randint(60, 100),
            student_id=student.id,
            teacher_id=subject.teacher_id,
            subject_id=subject.id,
            created=grade_date
        )
        session.add(grade)

session.commit()

session.close()


print(f"Студентів: {session.query(Student).count()}")
print(f"Викладачів: {session.query(Teacher).count()}")
print(f"Предметів: {session.query(Subject).count()}")
print(f"Оцінок: {session.query(Grade).count()}")
