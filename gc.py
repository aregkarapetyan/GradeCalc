# Libraries used in the program
import json
import hashlib

# Pre-defined variables
pass_attempts = 5
username_attempts  = 5

# Load Grade Setup Data
def load_setup_data():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)
    grades = course["course_setup"]["grade_breakdown"]
    conv_matrix = course["course_setup"]["conv_matrix"]
    return grades, conv_matrix

# Load Student grades
# Deals with cases if file is empty or doesn't exist
def load_grades_data():
    try:
        file = open('gc_grades.json', 'r+')
        if file.readlines() == []:
            file.write("{}")
            file.close()
    except Exception as e:
        file = open('gc_grades.json', 'w')
        file.write("{}")
        file.close()

    with open('gc_grades.json') as data_file:
        student_grades = json.load(data_file)

    return student_grades

# Load Student info
# Deals with cases if file is empty or doesn't exist
def load_data():
    try:
        file = open('gc_studinfo.json', 'r+')
        if file.readlines() == []:
            file.write("{}")
            file.close()
    except Exception as e:
        file = open('gc_studinfo.json', 'w')
        file.write("{}")
        file.close()

    with open('gc_studinfo.json') as data_file:
        data = json.load(data_file)

    return data

# Check if password is valid and return the correct one
def pass_validation(data, id, pass_attempts):
    password = hashlib.sha224(str(raw_input("Please insert your password: "))).hexdigest()
    while pass_attempts > 0:
        if password != str(data[id]["password"]):
            print "Access denied!\nYou have " + str(pass_attempts - 1) + " attempts left"
            password = hashlib.sha224(str(raw_input("Please insert your password: "))).hexdigest()
            pass_attempts -= 1
        elif password == str(data[id]["password"]):
            print "Access granted!"
            break
        else:
            print("Error in comparing passwords --- Error in pass_validation")
    if pass_attempts == 0:
        print("You exceeded the maximum amount of attempts")
        password = False
    return password

# Check if username is valid and return the correct one
def username_validation(data, id, username_attempts):
    username = raw_input("Please insert your username: ")
    while username_attempts > 0:
        if username != str(data[id]["username"]):
            print "Wrong username!\nYou have " + str(username_attempts - 1) + " attempts left"
            username = raw_input("Please insert your username: ")
            username_attempts -= 1
        elif username == str(data[id]["username"]):
            print "Access granted!"
            break
        else:
            print("Error in comparing usernames --- Error in username_validation")
    if username_attempts == 0:
        print("You exceeded the maximum amount of attempts")
        username = False
    return username

# Get list of grades for selected student
# If student don't have the grade yet, he should write 0, because contribution of that element is 0 at that moment
def askForAssignmentMarks(student_grades, grades, id,username, password):
    current_grades = {id:{}}
    for key in grades:
        if id in student_grades.keys():
            if student_grades[id][key] > "0":
                answ = raw_input("Your grade for " + key + " is " + str(student_grades[id][key]) + ". Do you want to change it? (Type yes)")
                if answ == "Yes" or answ == "yes" or answ == "y" or answ == "Y":
                    stud_grade = raw_input("Insert your grade for " + key + " ")
                    check_and_get_valid_number(stud_grade, current_grades, student_grades, id, key)
                else:
                    current_grades[id][key] = student_grades[id][key]
            elif student_grades[id][key] == "0":
                stud_grade = raw_input("You currently don't have a grade. What is your current grade for " + key + ". Insert 0 if you still don't have it.")
                check_and_get_valid_number(stud_grade, current_grades, student_grades, id, key)
        else:
            stud_grade = raw_input("What is your current grade for " + key + ". Insert 0 if you don't have it.")
            check_and_get_valid_number(stud_grade, current_grades, student_grades, id, key)
    return current_grades

# Check if the input is eligible(between 0 and 100)
def check_and_get_valid_number(stud_grade, current_grades, student_grades, id, key):
    status = stud_grade.isdigit()
    if status == False:
        print"Input a number between 0 and 100"
        stud_grade = raw_input("Insert your grade for " + key + " ")
        check_and_get_valid_number(stud_grade, current_grades, student_grades, id, key)
    elif status == True:
        stud_grade = int(stud_grade)
        if (stud_grade >= 0 and stud_grade <= 100):
            current_grades[id][key] = str(stud_grade)
        else:
            print "Input a number between 0 and 100"
            stud_grade = raw_input("Insert your grade for " + key + " ")
            check_and_get_valid_number(stud_grade, current_grades, student_grades, id, key)
    else:
        print "Error in checking the grade --- Error in check_and_get_valid_number"
    return stud_grade

# Write our changes in the initial file with students' grades
def save_grades(student_grades, current_grades):
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

# Write our changes in the initial file with students' data
def save_data(data,username, password, id, user_type):
    current_data = {id: {"username":username, "password": password, "type": user_type}}
    data[current_data.keys()[0]] = current_data[current_data.keys()[0]]
    file = open("gc_studinfo.json", "w")
    file.write(json.dumps(data))
    file.close()

# Calculates number grade
def print_current_grade(grades, current_grades, id,username):
    curr_grade = 0
    max_pos = 0
    for key in current_grades[id]:
        calc_grade = (float(current_grades[id][key]) * grades[key] / 100)
        if (float(current_grades[id][key]) == 0):
            calc_max = 0
        else:
            calc_max = float(grades[key])
        curr_grade = curr_grade + calc_grade
        max_pos = max_pos + calc_max
    return curr_grade, max_pos

# Gets the current letter grade, based on the number grade
# Prints both number and letter grades
def get_letter_grade(curr_grade, conv_matrix, id, data,username, max_pos):
    for i in range(len(conv_matrix)):
        if curr_grade >= int(conv_matrix[i]["min"]):
            print ("AUA ID: " + id + ", Student: " + username)
            print ("Your average grade is " + str(curr_grade) + " out of " + str(max_pos) + " or " + str(conv_matrix[i]["mark"]))
            break

# Lecturer has access to all grades if he wants so
def print_student_grades(student_grades, id,username):
    lectAns = raw_input("Lecturers can view everyone's grades. Do you want to view all grades?(Type yes)")
    if lectAns == "Yes" or lectAns == "yes" or lectAns == "y" or lectAns == "Y":
        print (json.dumps(student_grades, indent=4, sort_keys=True))
        #print "Student ID   Name    " +" "
        #print id + " "+username +" "+ student_grades[id]["Homeworks"]+" " + student_grades[id]["Quizes"] +" "+ student_grades[id]["Midterm 1"] +" "+ student_grades[id]["Midterm 2"] +" "+ student_grades[id]["Final Exam"]

# Heart of our program, which executes all functions in needed order
def main():
    grades, conv_matrix = load_setup_data()
    data = load_data()
    student_grades = load_grades_data()
    user_type = raw_input("Please tell if you are a student or teacher(s/t)")
    id = raw_input("Please insert your AUA ID: ")
    if user_type == "student" or user_type == "s" or user_type == "S" or user_type == "Student":
        user_type = "Student"
        if id in student_grades.keys():
            username = username_validation(data, id, username_attempts)
            if username != False:
                password = pass_validation(data, id, pass_attempts)
            else:
                password = False
        else:
            username = raw_input("Dear new user, please insert your username: ")
            password = hashlib.sha224(str(raw_input("Please insert your password: "))).hexdigest()
        if password == False:
            print("Try again later")
        else:
            current_grades = askForAssignmentMarks(student_grades, grades, id,username, password)
            save_grades(student_grades, current_grades)
            save_data(data,username, password, id, user_type)
            curr_grade, max_pos = print_current_grade(grades, current_grades, id,username)
            get_letter_grade(curr_grade, conv_matrix, id, data,username, max_pos)
    elif user_type == "teacher" or user_type == "t" or user_type == "T" or user_type == "Teacher":
        user_type = "Teacher"
        if id in data.keys():
            username = username_validation(data, id, username_attempts)
            if username != False:
                password = pass_validation(data, id, pass_attempts)
            else:
                password = False
        else:
            username = raw_input("Dear new user, please insert your username: ")
            password = hashlib.sha224(str(raw_input("Please insert your password: "))).hexdigest()
        if password == False:
            print("Try again later")
        else:
            print_student_grades(student_grades, id,username)
            save_data(data,username, password, id, user_type)
    else:
        print "Not valid input"

main()
