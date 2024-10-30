import json

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}")

class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []  # Store course codes instead of course names

    def add_grade(self, course_code, grade):
        self.grades[course_code] = grade

    def enroll_course(self, course_code):
        self.courses.append(course_code)

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}")
        print("Courses Enrolled:", ", ".join(self.courses))
        print("Grades:", self.grades)

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "address": self.address,
            "student_id": self.student_id,
            "grades": self.grades,
            "courses": self.courses
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"], data["age"], data["address"], data["student_id"])
        student.grades = data["grades"]
        student.courses = data["courses"]
        return student

class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def display_course_info(self):
        print(f"Course Name: {self.course_name}, Course Code: {self.course_code}, Instructor: {self.instructor}")
        print("Enrolled Students:", [student.name for student in self.students])

    def to_dict(self):
        return {
            "course_name": self.course_name,
            "course_code": self.course_code,
            "instructor": self.instructor,
            "students": [student.student_id for student in self.students]
        }

    @classmethod
    def from_dict(cls, data, students):
        course = cls(data["course_name"], data["course_code"], data["instructor"])
        course.students = [students[student_id] for student_id in data["students"]]
        return course

def add_student(students):
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    address = input("Enter address: ")
    student_id = input("Enter student ID: ")
    student = Student(name, age, address, student_id)
    students[student_id] = student
    print(f"Student {name} (ID: {student_id}) added successfully.")

def add_course(courses):
    course_name = input("Enter course name: ")
    course_code = input("Enter course code: ")
    instructor = input("Enter instructor name: ")
    course = Course(course_name, course_code, instructor)
    courses[course_code] = course
    print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")

def enroll_in_course(students, courses):
    student_id = input("Enter student ID: ")
    course_code = input("Enter course code: ")
    if student_id in students and course_code in courses:
        student = students[student_id]
        course = courses[course_code]
        student.enroll_course(course_code)
        course.add_student(student)
        print(f"Student {student.name} (ID: {student_id}) enrolled in course {course.course_name} (Code: {course_code}).")
    else:
        print("Invalid student ID or course code.")

def add_grade(students):
    student_id = input("Enter student ID: ")
    course_code = input("Enter course code: ")
    grade = input("Enter grade: ")
    if student_id in students:
        student = students[student_id]
        if course_code in student.courses:
            student.add_grade(course_code, grade)
            print(f"Grade {grade} added for student {student.name} (ID: {student_id}) in course {course_code}.")
        else:
            print("Student is not enrolled in this course.")
    else:
        print("Invalid student ID.")

def display_student_details(students):
    student_id = input("Enter student ID: ")
    if student_id in students:
        students[student_id].display_student_info()
    else:
        print("Student not found.")

def display_course_details(courses):
    course_code = input("Enter course code: ")
    if course_code in courses:
        courses[course_code].display_course_info()
    else:
        print("Course not found.")

def save_data(students, courses, filename="data.json"):
    data = {
        "students": {sid: student.to_dict() for sid, student in students.items()},
        "courses": {cc: course.to_dict() for cc, course in courses.items()}
    }
    with open(filename, 'w') as f:
        json.dump(data, f)
    print("Data saved successfully.")

def load_data(filename="data.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    students = {sid: Student.from_dict(details) for sid, details in data["students"].items()}
    courses = {cc: Course.from_dict(details, students) for cc, details in data["courses"].items()}
    print("Data loaded successfully.")
    return students, courses

def main():
    students = {}
    courses = {}

    # Load data at the start
    try:
        students, courses = load_data()
    except FileNotFoundError:
        print("No previous data found. Starting fresh.")

    while True:
        print("==== Student Management System ====\n1. Add Student\n2. Add Course\n3. Enroll in Course\n4. Add Grade\n5. Display Student Details\n6. Display Course Details\n7. Save Data\n8. Load Data\n0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student(students)
        elif choice == '2':
            add_course(courses)
        elif choice == '3':
            enroll_in_course(students, courses)
        elif choice == '4':
            add_grade(students)
        elif choice == '5':
            display_student_details(students)
        elif choice == '6':
            display_course_details(courses)
        elif choice == '7':
            save_data(students, courses)
        elif choice == '8':
            students, courses = load_data()
        elif choice == '0':
            save_data(students, courses)  # Save data before exiting
            print("Exiting the program. Data saved successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
