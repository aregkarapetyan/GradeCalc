# Libraries used in the program
import json


# Load Grade Setup Data
def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)
    grades = course["course_setup"]["grade_breakdown"]
    convMatrix = course["course_setup"]["conv_matrix"]
    return grades, convMatrix


# Load Students with their grades
# Deals with cases if file is empty or doesn't exist
def loadGradesData():
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

def askForStudentInfo():
    studentID = raw_input("Please insert your studentID: ")
    name = raw_input("Please insert your name: ")
    return studentID, name


# Get list of grades for selected student
# If student don't have the grade yet, he should write 0, because contribution of that element is 0 at that moment
def askForAssignmentMarks(student_grades, grades, studentID, name):
    current_grades = {studentID: {"name": name}}
    for key in grades:
        if studentID in student_grades.keys():
            if student_grades[studentID][key] > '-1':
                answ = raw_input("Your grade for " + key + " is " + str(
                    student_grades[studentID][key]) + ". Do you want to change it? (Type yes)")
                if answ == "Yes" or answ == "yes" or answ == "y" or answ == "Y":
                    stud_grade = raw_input("Insert your grade for " + key + " ")
                    checkIfValidNumber(stud_grade, current_grades, student_grades, studentID, key)
                else:
                    current_grades[studentID][key] = student_grades[studentID][key]
            else:
                stud_grade = raw_input(
                    "You currently don't have a grade. What is your current grade for " + key + ". Insert 0 if you still don't have it.")
                checkIfValidNumber(stud_grade, current_grades, student_grades, studentID, key)
        else:
            stud_grade = raw_input("What is your current grade for " + key + ". Insert 0 if you don't have it.")
            checkIfValidNumber(stud_grade, current_grades, student_grades, studentID, key)
    return current_grades


# Check if the input is eligible(between 0 and 100)
def checkIfValidNumber(stud_grade, current_grades, student_grades, studentID, key):
    status = stud_grade.isdigit()
    if status == False:
        print"Input a number between 0 and 100"
        stud_grade = raw_input("Insert your grade for " + key + " ")
        checkIfValidNumber(stud_grade, current_grades, student_grades, studentID, key)
    elif status == True:
        stud_grade = int(stud_grade)
        if (stud_grade >= 0 and stud_grade <= 100):
            current_grades[studentID][key] = str(stud_grade)
        else:
            print"Input a number between 0 and 100"
            stud_grade = raw_input("Insert your grade for " + key + " ")
            checkIfValidNumber(stud_grade, current_grades, student_grades, studentID, key)
    else:
        print "status error"
    return stud_grade


# Write our changes in the initial file with students
def saveGrades(student_grades, current_grades):
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()


# Calculates number grade
def printCurrentGrade(grades, current_grades, studentID, name):
    curr_grade = 0
    for key in current_grades[studentID]:
        if current_grades[studentID][key] != -1 and current_grades[studentID][key] != name:
            calc_grade = (float(current_grades[studentID][key]) * grades[key] / 100)
            curr_grade = curr_grade + calc_grade
    return curr_grade


# Gets the current letter grade, based on the number grade
# Prints both number and letter grades
def getLetterGrade(curr_grade, convMatrix, studentID, student_grades):
    for i in range(len(convMatrix)):
        if curr_grade >= int(convMatrix[i]["min"]):
            print ("AUA ID: " + studentID + ", Student: " + student_grades[studentID]["name"])
            print ("Your average grade is " + str(curr_grade) + " or " + str(convMatrix[i]["mark"]))
            break


# Lecturer has access to all grades if he wants so
def printStudentGrades(student_grades):
    lectAns = raw_input(
        "Lecturers can view everyone's grades. Do you want to view all grades?(Type yes)")
    if lectAns == "Yes" or lectAns == "yes" or lectAns == "y" or lectAns == "Y":
        print (json.dumps(student_grades, indent=4, sort_keys=True))


# Heart of our program, which executes all function in needed order
def main():
    grades, convMatrix = loadSetupData()
    user_type = raw_input("Please tell if you are a student or teacher")
    student_grades = loadGradesData()
    if user_type == "student":
        studentID, name = askForStudentInfo()
        current_grades = askForAssignmentMarks(student_grades, grades, studentID, name)
        saveGrades(student_grades, current_grades)
        curr_grade = printCurrentGrade(grades, current_grades, studentID, name)
        getLetterGrade(curr_grade, convMatrix, studentID, student_grades)
    else:
        printStudentGrades(student_grades)

main()
