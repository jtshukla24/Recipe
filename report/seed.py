from .models import *
import random
from faker import Faker
from django.db.models import Sum

fake = Faker()


def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0, 100)
                )
    except Exception as e:
        print(e)


def seed_db(n=10) -> None:
    try:
        for _ in range(n):
            department_objs = Department.objects.all()
            random_index = random.randint(0, len(department_objs) - 1)
            department = department_objs[random_index]
            student_id = f'STU-0{random.randint(100, 999)}'
            student_age = random.randint(20, 30)
            student_name = fake.name()
            student_email = fake.email()
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_email=student_email,
                student_name=student_name,
                student_address=student_address,
                student_age=student_age

            )

    except:
        pass


def generate_report_card():
    #current_rank = -1
    ranks = Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks', '-student_age')

    i = 1
    for rank in ranks:
        ReportCard.objects.create(
            student=rank,
            student_rank=i
        )
        i += 1
