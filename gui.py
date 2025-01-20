import backend
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Table functionality
import matplotlib.pyplot as plt


sort_order = "desc"

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x800")


# Function to handle adding a new student
def handle_add_student():
    add_window = tk.Toplevel(root)
    add_window.title(f"Add New Student")
    add_window.geometry("300x300")

    tk.Label(add_window, text="Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Math:").pack()
    math_entry = tk.Entry(add_window)
    math_entry.pack()

    tk.Label(add_window, text="Physiqaue:").pack()
    physique_entry = tk.Entry(add_window)
    physique_entry.pack()

    tk.Label(add_window, text="Philosophie:").pack()
    philo_entry = tk.Entry(add_window)
    philo_entry.pack()

    tk.Label(add_window, text="English:").pack()
    english_entry = tk.Entry(add_window)
    english_entry.pack()

    def confirm():

        try:
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("ERROR", "Name can't be empty")
                return
            math = float(math_entry.get())
            physique = float(physique_entry.get())
            philo = float(philo_entry.get())
            english = float(english_entry.get())

            for score in [math, physique, philo, english]:
                if not (0 <= score <= 20):
                    messagebox.showerror("Error", "Scores must be between 0 and 20!")
                    return
            backend.add_student(name, math, physique, philo, english)
            update_student_list()
            messagebox.showinfo("Success", "Student added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric scores between 0 and 20.")

    tk.Button(add_window, text="Confirm", command=confirm).pack(pady=5)


tk.Button(root, text="Add student", command=handle_add_student).pack(pady=5)


#Function to handle delete
def handle_delete_student():
    select_item = tree.selection()
    if not select_item:
        messagebox.showerror("ERROR", "Please select a student to delete")
        return
    student_name = tree.item(select_item, "values")[0]
    backend.delete_student(student_name)
    update_student_list()
    messagebox.showinfo("success", f"Deleted {student_name} successfully")


tk.Button(root, text="Delete Student", command=handle_delete_student).pack(pady=5)


def handle_edit_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("ERROR", "No student selected, please select to modify")
        return
    student_name = tree.item(selected_item, "values")[0]
    student_data = next((s for s in backend.students if s["name"] == student_name), None)
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit {student_name}")
    edit_window.geometry("300x300")

    #labels and entry fields for scores
    tk.Label(edit_window, text="Name:").pack()
    name_entry = tk.Entry(edit_window)
    name_entry.insert(0, student_data["name"])
    name_entry.pack()

    tk.Label(edit_window, text="Math:").pack()
    math_entry = tk.Entry(edit_window)
    math_entry.insert(0, student_data["math"])
    math_entry.pack()

    tk.Label(edit_window, text="Physique:").pack()
    physique_entry = tk.Entry(edit_window)
    physique_entry.insert(0, student_data["physique"])
    physique_entry.pack()

    tk.Label(edit_window, text="Philosophie:").pack()
    philo_entry = tk.Entry(edit_window)
    philo_entry.insert(0, student_data["philosophie"])
    philo_entry.pack()

    tk.Label(edit_window, text="English:").pack()
    english_entry = tk.Entry(edit_window)
    english_entry.insert(0, student_data["english"])
    english_entry.pack()

    def save_changes():
        try:
            new_name = name_entry.get()
            new_math = float(math_entry.get())
            new_physique = float(physique_entry.get())
            new_philo = float(philo_entry.get())
            new_english = float(english_entry.get())
            for score in [new_math, new_physique, new_philo, new_english]:
                if not (0 <= score <= 20):
                    messagebox.showerror("Error", "Scores must be between 0 and 20!")
                    return

            backend.edit_student(student_name, new_math, new_physique, new_philo, new_english, new_name)
            update_student_list()
            messagebox.showinfo("Success", f"Updated {student_name} successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric scores between 0 and 20.")

    tk.Button(edit_window, text="Save changes", command=save_changes).pack(pady=10)


tk.Button(root, text="Edit Student", command=handle_edit_student).pack(pady=5)


# Function to update student list in the GUI
def update_student_list():
    for row in tree.get_children():
        tree.delete(row)
    for student in backend.students:
        avg = backend.calculate_avg(student)
        grade = backend.assign_grade(avg)
        tree.insert("", "end", values=(student["name"], f"{avg:.2f}", grade))
    update_statistics()

# Function to sort students by average
def sort_student():
    global sort_order
    if sort_order == "desc":
        backend.students.sort(key=lambda student: backend.calculate_avg(student))
        sort_order = "asc"
    else:
        backend.students.sort(key=lambda student: backend.calculate_avg(student), reverse=True)
        sort_order = "desc"

    update_student_list()


tk.Button(root, text="Sort by Average (Toggle)", command=sort_student).pack(pady=5)

def handle_export():
    filename="students_export.csv"
    backend.export_to_csv(filename)
    messagebox.showinfo("Success",f"Student data exported to {filename}!")


def show_reports():
    if not backend.students:
        messagebox.showerror("Error", "No student data available!")
        return

    names = [student["name"] for student in backend.students]
    averages = [backend.calculate_avg(student) for student in backend.students]

    # Create bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(names, averages, color="blue")

    # Labels and title
    plt.xlabel("Students")
    plt.ylabel("Average Score")
    plt.title("Student Performance")
    plt.xticks(rotation=45, ha="right")  # Rotate labels for readability

    # Show chart
    plt.tight_layout()
    plt.show()

def update_statistics():
    class_avg=backend.calculate_calss_average()
    top_student = backend.find_top_student()
    lowest_student = backend.find_lowest_student()

    class_avg_label.config(text=f"Class Average:{class_avg:.2f}")
    if top_student:
        top_student_label.config(text=f"Top Student: {top_student['name']} ({backend.calculate_avg(top_student):.2f})")
    else:
        top_student_label.config(text="Top student: N/A")
    if lowest_student:
        lowest_student_label.config(
            text=f"Lowest Performer: {lowest_student['name']} ({backend.calculate_avg(lowest_student):.2f})")
    else:
        lowest_student_label.config(text="Lowest Performer: N/A")
tk.Button(root, text="Export to CSV", command=handle_export).pack(pady=5)
tk.Button(root, text="Show Reports", command=show_reports).pack(pady=5)


class_avg_label = tk.Label(root, text="Class Average: N/A", font=("Arial", 12))
class_avg_label.pack()

top_student_label = tk.Label(root, text="Top Student: N/A", font=("Arial", 12))
top_student_label.pack()

lowest_student_label = tk.Label(root, text="Lowest Performer: N/A", font=("Arial", 12))
lowest_student_label.pack()


# Student Table
columns = ("Name", "Average", "Grade")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack()


# Load students from CSV and display them in the table
backend.load_students()
update_student_list()

root.mainloop()
