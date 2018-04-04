import json

def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)

    grades = course["course_setup"]["grade_breakdown"]
    convMatrix = course["course_setup"]["conv_matrix"]
    return grades, convMatrix

def loadGradesData():
    with open('gc_grades.json') as data_file:
        student_grades = json.load(data_file) 
    name = raw_input("Please insert your name: ")

    return student_grades, name

def askForAssignmentMarks(student_grades,grades,name):
    current_grades = {name:{}}
    for key in grades:
        if student_grades[name][key] > '-1':
            answ = raw_input("Your grade for " + key + " is " + str(student_grades[name][key]) + ". Do you want to change it?")
            if answ == "Yes" or answ == "yes" or answ == "y" or answ == "Y":
                stud_grade = raw_input("Insert your grade for " + key + " ")
                stud_grade = int(stud_grade)
                if (stud_grade >= 0 and stud_grade <= 100) or stud_grade == '-1':
                    current_grades[name][key] = str(stud_grade)
                else:
                    print"Input a number between 0 and 100"
                    current_grades[name][key] = student_grades[name][key]
            else:
                current_grades[name][key] = student_grades[name][key]
        else:
            stud_grade = raw_input("What is your current grade for " + key + ". Insert -1 if you don't have it.")
            stud_grade = int(stud_grade)
            if stud_grade >= 0 or stud_grade<=100 or stud_grade == -1:
                current_grades[name][key] = str(stud_grade)
            else:
                print"Input a number between 0 and 100"
                current_grades[name][key] = student_grades[name][key]
    return current_grades

def saveGrades(student_grades, current_grades):
    student_grades[current_grades.keys()[0]]=current_grades[current_grades.keys()[0]]
    #print (json.dumps(student_grades))
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def printCurrentGrade(grades, current_grades, name):
    curr_grade = 0
    for key in current_grades[name]:
        if current_grades[name][key] != -1:
            calc_grade = (float(current_grades[name][key]) * grades[key] / 100)
            curr_grade = curr_grade + calc_grade
    return curr_grade

def getLetterGrade(curr_grade, convMatrix):
    for i in range(len(convMatrix)):
        if curr_grade >= int(convMatrix[i]["min"]):
            print ("Your average grade is " + str(curr_grade) + " or " + str(convMatrix[i]["mark"]))
            break
def main():
    grades, convMatrix = loadSetupData()
    student_grades, name = loadGradesData()
    current_grades = askForAssignmentMarks(student_grades, grades, name)
    saveGrades(student_grades, current_grades)
    curr_grade = printCurrentGrade(grades, current_grades, name)
    getLetterGrade(curr_grade,convMatrix)

main()