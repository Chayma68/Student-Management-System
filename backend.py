import csv
import os

import backend

students = [
    {"name": "khadija alaoui", "math": 19, "physique": 18, "philosophie": 16, "english": 17},
    {"name": "amine mdghri", "math": 13, "physique": 15, "philosophie": 17, "english": 14},
    {"name": "ahmed ouali", "math": 20, "physique": 18.5, "philosophie": 17, "english": 19},
    {"name": "salma fassi", "math": 16, "physique": 14.5, "philosophie": 18, "english": 15},
    {"name": "mohamed taha", "math": 12, "physique": 10, "philosophie": 14, "english": 13},
    {"name": "imane chafik", "math": 17.5, "physique": 19, "philosophie": 16, "english": 18},
    {"name": "hamza el baraka", "math": 14, "physique": 15, "philosophie": 15.5, "english": 14.5},
    {"name": "sara bennis", "math": 18.5, "physique": 17, "philosophie": 16, "english": 18},
    {"name": "mehdi benjelloun", "math": 11, "physique": 13, "philosophie": 12, "english": 10},
    {"name": "hajar mekkaoui", "math": 15.5, "physique": 16, "philosophie": 14, "english": 16.5},
]


# Function to validate scores
def score_validation(student):
    for subject, score in student.items():
        if subject != "name" and ((not isinstance(score, (int, float))) or not 0 <= score <= 20):
            raise ValueError(f"Invalid score '{score}' for {subject} in {student['name']}.")


# Function to calculate the average for a student
def calculate_avg(student):
    score_validation(student)
    scores = [student["math"], student["physique"], student["philosophie"], student["english"]]
    return sum(scores) / len(scores)


# Function to assign grades based on the Moroccan grading system
def assign_grade(avg):
    if 16 <= avg <= 20:
        return "Très Bien"
    elif 14 <= avg < 16:
        return "Bien"
    elif 12 <= avg < 14:
        return "Assez Bien"
    elif 10 <= avg < 12:
        return "Passable"
    elif avg < 10:
        return "Insuffisant (Échec)"
    else:
        return "Error"


# Function to save students to a CSV file
def save_students():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "math", "physique", "philosophie", "english"])
        for student in students:
            writer.writerow([
                student["name"],
                student["math"],
                student["physique"],
                student["philosophie"],
                student["english"]
            ])
        print("Students saved successfully!")


# Function to load students from CSV file
def load_students():
    global students
    if os.path.exists("students.csv"):
        with open("students.csv", "r") as file:
            reader = csv.DictReader(file)
            students.clear()
            for row in reader:
                if row["name"].strip():  # Avoid empty rows
                    students.append({
                        "name": row["name"].strip(),
                        "math": float(row["math"]),
                        "physique": float(row["physique"]),
                        "philosophie": float(row["philosophie"]),
                        "english": float(row["english"]),
                    })


# Function to add a new student
def add_student(name, math, physique, philo, english):
    student = {
        "name": name,
        "math": math,
        "physique": physique,
        "philosophie": philo,
        "english": english
    }
    students.append(student)
    save_students()


def delete_student(name):
    global students
    students = [student for student in students if student["name"] != name]
    save_students()


def edit_student(name, new_math, new_physique, new_philo, new_english, new_name):
    for student in students:
        if student["name"] == name:
            student["name"] = new_name
            student["math"] = new_math
            student["physique"] = new_physique
            student["philosophie"] = new_philo
            student["english"] = new_english
            break

    save_students()


#Function to export data to csv
def export_to_csv(filename="export_students.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Math", "Physique", "Philosophie", "English"])
        for student in students:
            avg = backend.calculate_avg(student)
            grade = assign_grade(avg)
            writer.writerow([
                student["name"],
                student["math"],
                student["physique"],
                student["philosophie"],
                student["english"],
                avg,
                grade
            ])

    print(f"Results successfully saved to {filename}!")


#Function to calculate the calss average
def calculate_calss_average():
    if not students:
        return 0
    total = sum(calculate_avg(student)for student in students)
    return total/len(students)


#Function to return Top student
def find_top_student():
    if not students:
        return None
    return max(students, key=lambda s:calculate_avg(s))


#Function to return lowest student
def find_lowest_student():
    if not students:
        return None
    return min(students, key=lambda s : calculate_avg(s))


# Ensure students are loaded when the module is imported
load_students()
