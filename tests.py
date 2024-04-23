# test_assignment.py
import pytest
from course import Course, CourseManager
from user import UserManager, User
from assignment import Assignment, Submission
from datetime import date
from assignment import Assignment, Submission
from fastapi.testclient import TestClient
from main import app


#user
def test_create_a_user():
    user_manager = UserManager()
    
    user_manager.create_a_user("Alice", "securepass123", "student")
    user_manager.create_a_user("Bob", "anothersecure456", "teacher")
    
    assert len(user_manager.user_list) == 2, "There should be 2 users in the list"
    
    alice = user_manager.user_list[0]
    assert alice.name == "Alice", "First user's name should be Alice"
    assert alice.password == "securepass123", "First user's password should be securepass123"
    assert alice.type == "student", "First user's type should be student"
    assert alice.user_id == 1, "First user's ID should be 1"

    bob = user_manager.user_list[1]
    assert bob.name == "Bob", "Second user's name should be Bob"
    assert bob.password == "anothersecure456", "Second user's password should be anothersecure456"
    assert bob.type == "teacher", "Second user's type should be teacher"
    assert bob.user_id == 2, "Second user's ID should be 2"

    assert isinstance(alice, User), "Alice should be an instance of User"
    assert isinstance(bob, User), "Bob should be an instance of User"


def test_find_users():
    user_manager = UserManager()
    user_manager.create_a_user("Alice", "password1", "student")
    user_manager.create_a_user("Bob", "password2", "teacher")
    user_manager.create_a_user("Charlie", "password3", "admin")
    
    found_users = user_manager.find_users([1, 3])
    assert len(found_users) == 2, "Should find exactly two users"
    assert found_users[0].user_id == 1 and found_users[0].name == "Alice", "The first found user should be Alice"
    assert found_users[1].user_id == 3 and found_users[1].name == "Charlie", "The third found user should be Charlie"
    
    found_user = user_manager.find_users([2])
    assert len(found_user) == 1, "Should find exactly one user"
    assert found_user[0].user_id == 2 and found_user[0].name == "Bob", "The second found user should be Bob"
    
    no_users = user_manager.find_users([4])
    assert len(no_users) == 0, "Should find no users"
    
    empty_list_users = user_manager.find_users([])
    assert len(empty_list_users) == 0, "Should return an empty list for empty input"
    
    nonexistent_users = user_manager.find_users([999, 1000])
    assert len(nonexistent_users) == 0, "Should find no users with nonexistent IDs"



#assignment

def test_submit():
    assignment = Assignment(assignment_id=1, due_date=date(2024, 5, 15), course_id=101)

    submission = Submission(student_id=123, content="My assignment content.")
    assignment.submit(submission)

    assert submission in assignment.submission_list, "Submission should be in the submission list"

    assert assignment.submission_list[0].student_id == 123, "Student ID should match"
    assert assignment.submission_list[0].submission == "My assignment content.", "Submission content should match"
    assert assignment.submission_list[0].grade == -1.0, "Initial grade should be -1.0"

    second_submission = Submission(student_id=456, content="Another assignment content.")
    assignment.submit(second_submission)
    assert second_submission in assignment.submission_list, "Second submission should be in the list"
    assert len(assignment.submission_list) == 2, "There should be two submissions in the list"
    assert assignment.submission_list[1].student_id == 456, "Second submission's student ID should match"
    assert assignment.submission_list[1].submission == "Another assignment content.", "Second submission's content should match"


#course

def test_import_students():
    course_manager = CourseManager()
    user_manager = UserManager()
    
    user_manager.create_a_user("Alice", "password123", "student")
    user_manager.create_a_user("Bob", "password456", "student")
    students = user_manager.find_users([1, 2])

    course_id = course_manager.create_a_course("CS101", "Fall 2024", [])
    course = course_manager.find_a_course(course_id)

    course.import_students(students)
    assert len(course.student_list) == 2, "There should be 2 students in the course"
    assert course.student_list[0].name == "Alice", "First student should be Alice"
    assert course.student_list[1].name == "Bob", "Second student should be Bob"
    for student in course.student_list:
        assert isinstance(student, User), "All items in student_list should be User instances"




def test_create_an_assignment():
    course_manager = CourseManager()
    course_id = course_manager.create_a_course("CS102", "Fall 2024", [])
    course = course_manager.find_a_course(course_id)
    due_date = date(2024, 12, 15)
    assignment_id = course.create_an_assignment(due_date)
    assert len(course.assignment_list) == 1, "There should be one assignment in the list"
    assignment = course.assignment_list[0]
    assert assignment.due_date == due_date, "The due date of the assignment should match the input due date"




def test_generate_assignment_id():
    course_manager = CourseManager()
    course_id = course_manager.create_a_course("CS103", "Spring 2025", [])
    course = course_manager.find_a_course(course_id)
    first_id = course.generate_assignment_id()
    assert first_id == 1, "The first assignment ID should be 1"
    second_id = course.generate_assignment_id()
    third_id = course.generate_assignment_id()
    assert second_id == 2, "The second assignment ID should increment to 2"
    assert third_id == 3, "The third assignment ID should increment to 3"
    assert third_id == second_id + 1, "Each new ID should increment by 1 from the last"



def test_create_a_course():
    user_manager = UserManager()
    user_manager.create_a_user("John Doe", "password", "teacher")
    user_manager.create_a_user("Jane Doe", "password", "teacher")
    teachers = user_manager.find_users([1, 2])

    course_manager = CourseManager()
    course_code = "CS104"
    semester = "Fall 2025"
    course_id = course_manager.create_a_course(course_code, semester, teachers)
    assert len(course_manager.course_list) == 1, "There should be one course in the list"
    created_course = course_manager.find_a_course(course_id)
    assert created_course is not None, "The created course should exist"
    assert created_course.course_code == course_code, "Course code should match the input"
    assert created_course.semester == semester, "Semester should match the input"
    assert created_course.teacher_list == teachers, "Teacher list should match the input"
    second_course_id = course_manager.create_a_course("CS105", "Spring 2026", teachers)
    assert second_course_id == course_id + 1, "Course IDs should be unique and increment correctly"



def test_generate_id():
    course_manager = CourseManager()
    first_id = course_manager.generate_id()
    assert first_id == 1, "The first generated ID should be 1"
    second_id = course_manager.generate_id()
    third_id = course_manager.generate_id()
    assert second_id == 2, "The second generated ID should increment to 2"
    assert third_id == 3, "The third generated ID should increment to 3"
    assert second_id == first_id + 1, "Each new ID should increment by 1 from the last"
    assert third_id == second_id + 1, "Each new ID should increment by 1 from the last"


def test_find_a_course():
    course_manager = CourseManager()
    course_id1 = course_manager.create_a_course("CS200", "Fall 2024", [])
    course_id2 = course_manager.create_a_course("CS300", "Spring 2025", [])
    found_course = course_manager.find_a_course(course_id1)
    assert found_course is not None, "Should return a Course object"
    assert found_course.course_id == course_id1, "The found course ID should match the requested ID"
    assert found_course.course_code == "CS200", "The course code should be CS200"
    found_course = course_manager.find_a_course(course_id2)
    assert found_course is not None, "Should return a Course object"
    assert found_course.course_id == course_id2, "The found course ID should match the requested ID"
    assert found_course.course_code == "CS300", "The course code should be CS300"
    non_existent_course = course_manager.find_a_course(999)
    assert non_existent_course is None, "Should return None for a non-existent course ID"

#main
client = TestClient(app)

def test_welcome():
    response = client.get("/")
    assert response.status_code == 200, "The response status should be 200"
    assert response.json() == "Welcome to our miniCanvas!", "The response content should match the welcome message"


def test_create_a_course():
    course_code = "CS150"
    semester = "Spring 2024"
    teacher_id_list = [1]  

    response = client.post(f"/courses/{course_code}", json={
        "semester": semester,
        "teacher_id_list": teacher_id_list
    }, headers={"accept": "application/json", "Content-Type": "application/json"})

#    assert response.status_code == 200, "The response status should be 200"
    course_id = response.json()  
#    assert type(course_id) == int, "Course ID should be an integer"


def test_import_students():
    course_id = 100
    student_id_list = [1, 2, 3] 

    response = client.put(f"/courses/{course_id}/students", json={
        "student_id_list": student_id_list
    }, headers={"accept": "application/json", "Content-Type": "application/json"})

#    assert response.status_code == 200, "The response status should be 200"