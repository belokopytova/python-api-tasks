from decorator2 import logger

class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    @logger('log_4.log')
    def avr_grade(self):
        b = []
        for v in self.grades.values():
            b += v
        return sum(b)/len(b)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.avr_grade()}\n'
                f'Курсы в процессе изучения: {",".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {",".join(self.finished_courses)}')

    def __eq__(self, other):
        a = sum(sum(other.grades.values(),[]))/len(sum(other.grades.values(),[]))
        return self.avr_grade() == a

    def __lt__(self, other):
        a = sum(sum(other.grades.values(),[]))/len(sum(other.grades.values(),[]))
        return self.avr_grade() < a

    def __gt__(self, other):
        a = sum(sum(other.grades.values(),[]))/len(sum(other.grades.values(),[]))
        return self.avr_grade() > a

    def give_grades_to_lecturer(self, lecturer, course, grade):

        if (isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and
            course in self.courses_in_progress):
            if course in lecturer.grades_of_lecturer:
                lecturer.grades_of_lecturer[course] += [grade]
            else:
                lecturer.grades_of_lecturer[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades_of_lecturer = {}

    def avr_grade(self):
        b = []
        for v in self.grades_of_lecturer.values():
            b += v
        return sum(b)/len(b)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.avr_grade()}')

    def __eq__(self, other):
        a = sum(sum(other.grades_of_lecturer.values(),[]))/len(sum(other.grades_of_lecturer.values(),[]))
        return self.avr_grade() == a

    def __lt__(self, other):
        a = sum(sum(other.grades_of_lecturer.values(),[]))/len(sum(other.grades_of_lecturer.values(),[]))
        return self.avr_grade() < a

    def __gt__(self, other):
        a = sum(sum(other.grades_of_lecturer.values(),[]))/len(sum(other.grades_of_lecturer.values(),[]))
        return self.avr_grade() > a


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')

    def give_grades(self, student, course, grade):

        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


student_1 = Student('Ruoy', 'Eman', 'your_gender')
student_1.courses_in_progress += ['Python', 'Java']
student_1.finished_courses += ['Алгоритмы']
student_2 = Student('Anna', 'Ivanova', 'female')
student_2.courses_in_progress += ['Git', 'Java' , 'Алгоритмы', 'Kotlin','Python']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python','Java']
reviewer_Tom = Reviewer('Tom', 'Smith')
reviewer_Tom.courses_attached += ['Java','Git', 'Алгоритмы']

lecturer_Bob = Lecturer('Bob', 'Fischer')
lecturer_Bob.courses_attached += ['Java', 'Git' , 'C++']
lecturer_Mary = Lecturer('Maria', 'Petrova')
lecturer_Mary.courses_attached += ['Python', 'Kotlin' , 'Алгоритмы', 'Java']

for i in range(3):
    cool_reviewer.give_grades(student_1, 'Python', 10)

reviewer_Tom.give_grades(student_1, 'Java', 5)
reviewer_Tom.give_grades(student_1, 'Java', 10)

reviewer_Tom.give_grades(student_2, 'Git', 8)
reviewer_Tom.give_grades(student_2, 'Алгоритмы', 10)
cool_reviewer.give_grades(student_2, 'Java', 10)
cool_reviewer.give_grades(student_2, 'Java', 8)


student_1.give_grades_to_lecturer(lecturer_Bob, 'Java', 8)
student_2.give_grades_to_lecturer(lecturer_Bob, 'Java', 10)
student_1.give_grades_to_lecturer(lecturer_Mary, 'Python', 5)
student_2.give_grades_to_lecturer(lecturer_Mary, 'Kotlin', 7)
student_2.give_grades_to_lecturer(lecturer_Mary, 'Java', 9)

print(student_1)
print(student_2)
print(lecturer_Bob)
print(lecturer_Mary)
print(cool_reviewer)
print(reviewer_Tom)

print(student_1 == student_2)
print(student_1 > student_2)
print(student_1 < student_2)

print(lecturer_Bob == lecturer_Mary)
print(lecturer_Bob > lecturer_Mary)
print(lecturer_Bob < lecturer_Mary)


#Задание № 4
student_list = [student_1,student_2]
lecturer_list = [lecturer_Bob,lecturer_Mary]

def avr_grade_students(list_of_students, name_course: str):
    cur = []
    for student in list_of_students:
        if name_course in student.grades:
            cur += student.grades[name_course]
        else:
            return "Нет такого курса у студента"
    avr = sum(cur)/len(cur)
    return avr

def avr_grade_lecturer(list_of_lecturers, name_course: str):
    cur = []
    for lecturer in list_of_lecturers:
        if name_course in lecturer.grades_of_lecturer:
            cur += lecturer.grades_of_lecturer[name_course]
        else:
            return "Нет такого курса у лектора"
    avr = sum(cur)/len(cur)
    return avr

print(avr_grade_students(student_list, 'Java'))
print(avr_grade_lecturer(lecturer_list, 'Java'))