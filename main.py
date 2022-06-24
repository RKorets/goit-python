from typing import Dict, List, Tuple
from collections import namedtuple, defaultdict
from datetime import datetime
import faker
from random import randint, choice

import sqlite3

NUMBER_GROUP = 3
NUMBER_STUDENT = 30
NUMBER_SUBJECTS = 5
NUMBER_TEACHERS = 3

conn = sqlite3.connect("student.sqlite3")
cursor = conn.cursor()


def generate_fake_data():
    fake_student = []
    fake_group = []
    fake_subject_data = []
    fake_teachers = []
    scoreboards = []

    fake_data = faker.Faker('uk-UA')

    for i in range(NUMBER_STUDENT):
        if i < 10:
            fake_student.append((f'{fake_data.last_name_female()} {fake_data.first_name_female()}', 1))
        elif 10 <= i < 20:
            fake_student.append((f'{fake_data.last_name_male()} {fake_data.first_name_male()}', 2))
        else:
            fake_student.append((f'{fake_data.last_name_male()} {fake_data.first_name_male()}', 3))

    for name in ['AKIT', 'FEMP', 'EEAT']:
        fake_group.append((name,))

    for teacher in ['Борисюк Т.', 'Тарасюк С.', 'Василюк П.']:
        fake_teachers.append((teacher,))

    for subject in ['МАТЕМАТИКА', 'ІСТОРІЯ', 'ІНФОРМАТИКА', 'АНГЛІЙСЬКА МОВА', 'ФІЗКУЛЬТУРА']:
        fake_subject_data.append((subject, randint(1, 3)))

    for students in range(1, NUMBER_STUDENT + 1):
        for lesson in range(1, NUMBER_SUBJECTS + 1):
            for _ in range(0, 20):
                mark_date = datetime(2021, randint(1, 12), randint(1, 28)).date()
                scoreboards.append((lesson, students, mark_date, randint(1, 12)))

    return fake_student, fake_group, fake_teachers, fake_subject_data, scoreboards


def insert_data_to_db(students, groups, teachers, subject_data, scoreboard) -> None:
    sql_to_student = """INSERT INTO student(studentName, groupId)
                               VALUES (?, ?)"""

    cursor.executemany(sql_to_student, students)

    sql_to_group = """INSERT INTO studentGroup(groupName)
                               VALUES (?)"""
    cursor.executemany(sql_to_group, groups)

    sql_to_teachers = """INSERT INTO teachers(teacherName)
                              VALUES (?)"""

    cursor.executemany(sql_to_teachers, teachers)

    sql_to_subjects = """INSERT INTO subjects(subjectName, idTeacher)
                                      VALUES (?, ?)"""

    cursor.executemany(sql_to_subjects, subject_data)

    sql_to_scoreboard = """INSERT INTO scoreboard(idSubject, idStudent, markDate, mark)
                                          VALUES (?, ?, ?, ?)"""

    cursor.executemany(sql_to_scoreboard, scoreboard)

    conn.commit()


def _init_db():
    with open("student.sql", "r") as f:
        sql = f.read()
    print("DB init")
    cursor.executescript(sql)
    conn.commit()
    student, group, teachers, subject_data, scoreboard = generate_fake_data()
    insert_data_to_db(student, group, teachers, subject_data, scoreboard)


def check_db_exists():
    cursor.execute("SELECT * FROM sqlite_master")
    table_exists = cursor.fetchall()
    if table_exists:
        print("DB exist")
        return
    _init_db()


def max_mark():
    student_mark = " SELECT student.studentName, AVG(scoreboard.mark) as Mark FROM scoreboard " \
                   "JOIN student ON student.id = scoreboard.idStudent" \
                   " GROUP by student.studentName" \
                   " ORDER by Mark DESC" \
                   " LIMIT 5"
    cursor.execute(student_mark)

    rows = cursor.fetchall()
    print('\n5 студентов с наибольшим средним баллом по всем предметам.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def one_max_mark_subject(subject: str):
    mark_subject = " SELECT subjects.subjectName, student.studentName, AVG(scoreboard.mark) as Mark FROM scoreboard " \
                   "JOIN student ON student.id = scoreboard.idStudent" \
                   " JOIN subjects ON subjects.idSubject = scoreboard.idSubject" \
                   f" WHERE subjects.subjectName = '{subject}'" \
                   " GROUP by student.studentName, subjects.subjectName" \
                   " ORDER by Mark DESC LIMIT 1"
    cursor.execute(mark_subject)
    rows = cursor.fetchall()
    print(f'\n1 студент с наивысшим средним баллом по предмету {subject}.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def avg_subjects():
    avg_subject = " SELECT subjects.subjectName, AVG(scoreboard.mark) as Mark FROM scoreboard " \
                  "JOIN subjects ON subjects.idSubject = scoreboard.idSubject" \
                  " GROUP by subjects.subjectName" \
                  " ORDER by Mark DESC"
    cursor.execute(avg_subject)
    rows = cursor.fetchall()
    print('\nCредний балл в группе по одному предмету')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def avg_group():
    avg_groups = " SELECT studentGroup.groupName, AVG(scoreboard.mark) as Mark FROM scoreboard " \
                 "JOIN student ON student.id = scoreboard.idStudent" \
                 " JOIN studentGroup ON student.groupId = studentGroup.idGroup" \
                 " GROUP by studentGroup.groupName" \
                 " ORDER by Mark DESC"
    cursor.execute(avg_groups)
    rows = cursor.fetchall()
    print('\nСредний балл в потоке.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def teacher_subjects():
    teacher_subject = " SELECT teachers.teacherName, subjects.subjectName FROM subjects " \
                      "JOIN teachers ON teachers.idTeachers = subjects.idTeacher" \
                      " GROUP by subjects.subjectName"
    cursor.execute(teacher_subject)
    rows = cursor.fetchall()
    print('\nКакие курсы читает преподаватель.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def student_in_group(group: str):
    student = " SELECT studentGroup.groupName, student.studentName FROM student " \
              "JOIN studentGroup ON studentGroup.idGroup = student.groupId" \
              f" WHERE studentGroup.groupName = '{group}'" \
              " GROUP by student.studentName"
    cursor.execute(student)
    rows = cursor.fetchall()
    print(f'\nСписок студентов в группе {group}.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def student_mark_in_group(group: str, subject: str):
    st = " SELECT studentGroup.groupName, subjects.subjectName, student.studentName, scoreboard.mark FROM student " \
              "JOIN studentGroup ON studentGroup.idGroup = student.groupId" \
              " JOIN scoreboard ON scoreboard.idStudent = student.id" \
              " JOIN subjects ON scoreboard.idSubject = subjects.idSubject" \
              f" WHERE studentGroup.groupName = '{group}' and subjects.subjectName= '{subject}' "
    cursor.execute(st)
    rows = cursor.fetchall()
    print(f'\nОценки студентов в группе {group} по предмету {subject}.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def student_last_mark(group: str, subject: str):
    student = "SELECT studentGroup.groupName, subjects.subjectName, student.studentName, " \
              "scoreboard.mark, MAX(scoreboard.markDate) FROM student " \
              "JOIN studentGroup ON studentGroup.idGroup = student.groupId" \
              " JOIN scoreboard ON scoreboard.idStudent = student.id" \
              " JOIN subjects ON scoreboard.idSubject = subjects.idSubject" \
              f" WHERE studentGroup.groupName = '{group}' and subjects.subjectName= '{subject}'" \
              " GROUP by student.studentName" \
              " ORDER BY scoreboard.markDate DESC"

    cursor.execute(student)
    rows = cursor.fetchall()
    print(f'\nОценки студентов в группе {group} по предмету {subject} на последнем занятии.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def student_teacher_list(student: str, teacher: str):
    student_subject = "SELECT subjects.subjectName FROM student " \
              " JOIN scoreboard ON scoreboard.idStudent = student.id" \
              " JOIN subjects ON scoreboard.idSubject = subjects.idSubject" \
              " JOIN teachers ON teachers.idTeachers = subjects.idTeacher" \
              f" WHERE student.studentName = '{student}' and teachers.teacherName= '{teacher}'" \
              " GROUP by subjects.subjectName"
    cursor.execute(student_subject)
    rows = cursor.fetchall()
    print(f'\nСписок курсов, которые студенту {student} читает преподаватель {teacher}.')
    for index, result in enumerate(rows, start=1):
        print(f'{index}. {result}')


def avg_teacher_marks_in_subject(teacher: str, subject: str):
    avg_teacher = "SELECT subjects.subjectName,student.studentName, AVG(scoreboard.mark) FROM scoreboard " \
              " JOIN student ON scoreboard.idStudent = student.id" \
              " JOIN subjects ON scoreboard.idSubject = subjects.idSubject" \
              " JOIN teachers ON teachers.idTeachers = subjects.idTeacher" \
              f" WHERE teachers.teacherName = '{teacher}' and subjects.subjectName = '{subject}'" \
              " GROUP by student.studentName"
    cursor.execute(avg_teacher)
    rows = cursor.fetchall()
    if len(rows):
        print(f'\nСредний балл, который преподаватель {teacher} ставит студенту.')
        for index, result in enumerate(rows, start=1):
            print(f'{index}. {result}')
    else:
        print(f'\nПреподаватель или предмет указан не верно')


def avg_teacher_marks(teacher: str):
    avg_teacher = "SELECT AVG(scoreboard.mark) FROM scoreboard " \
              " JOIN subjects ON scoreboard.idSubject = subjects.idSubject" \
              " JOIN teachers ON teachers.idTeachers = subjects.idTeacher" \
              f" WHERE teachers.teacherName = '{teacher}'" \

    cursor.execute(avg_teacher)
    rows = cursor.fetchall()
    if len(rows):
        print(f'\nСредний балл, который ставит преподаватель {teacher}.')
        for index, result in enumerate(rows, start=1):
            print(f'{index}. {result}')
    else:
        print(f'\nПреподавателя с таким именем не найдено')


if __name__ == '__main__':
    check_db_exists()
    max_mark()
    one_max_mark_subject('ФІЗКУЛЬТУРА')
    avg_subjects()
    avg_group()
    teacher_subjects()
    student_in_group('EEAT')
    student_mark_in_group('AKIT', 'МАТЕМАТИКА')
    student_last_mark('FEMP', 'МАТЕМАТИКА')
    student_teacher_list('Василашко Михайлина', 'Василюк П.')
    avg_teacher_marks_in_subject('Тарасюк С.', 'МАТЕМАТИКА')
    avg_teacher_marks('Тарасюк С.')

