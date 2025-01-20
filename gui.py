import backend
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Table functionality
import matplotlib.pyplot as plt
from ttkthemes import ThemedTk

sort_order = "desc"

# Main window
root = ThemedTk(theme="arc")
root.title("Student Management System")
root.geometry("650x600")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

#Frame: Buttons
button_frame = ttk.Frame(root, padding=10)
button_frame.pack()

ttk.Button(button_frame, text="Add Student", command=lambda: handle_add_student()).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Edit Student", command=lambda: handle_edit_student()).grid(row=0, column=1, padx=5,
                                                                                          pady=5)
ttk.Button(button_frame, text="Delete Student", command=lambda: handle_delete_student()).grid(row=0, column=2, padx=5,
                                                                                              pady=5)
ttk.Button(button_frame, text="Sort Students", command=lambda: sort_order).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(button_frame, text="Export CSV", command=lambda: handle_export).grid(row=0, column=4, padx=5, pady=5)

#Frame:  statistics

stats_frame = ttk.Frame(root, padding=10)
stats_frame.pack()

class_avg_label = ttk.Label(stats_frame, text="Class Average: N/A", font=("Arial", 12))
class_avg_label.grid(row=0, column=0, padx=10)

top_student_label = ttk.Label(stats_frame, text="Top Student: N/A", font=("Arial", 12))
top_student_label.grid(row=0, column=1, padx=10)

lowest_student_label = ttk.Label(stats_frame, text="Lowest Performer: N/A", font=("Arial", 12))
lowest_student_label.grid(row=0, column=2, padx=10)

#Frame : student Table
table_frame = ttk.Frame(root, padding=10)
table_frame.pack(fill="both", expand=True)


# Function to handle adding a new student
def handle_add_student():
    add_window = tk.Toplevel(root)
    add_window.title(f"Add New Student")
    add_window.geometry("300x300")
    add_window.configure(bg="#edd5e4")


    style = ttk.Style()
    style.configure("Custom.TFrame", background="#edd5e4")

    frame = ttk.Frame(add_window, padding=10, style="Custom.TFrame")
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Name:", background="#edd5e4").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Math:", background="#edd5e4").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    math_entry = ttk.Entry(frame)
    math_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Physique:", background="#edd5e4").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    physique_entry = ttk.Entry(frame)
    physique_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Philosophie:", background="#edd5e4").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    philo_entry = ttk.Entry(frame)
    philo_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="English:", background="#edd5e4").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    english_entry = ttk.Entry(frame)
    english_entry.grid(row=4, column=1, padx=5, pady=5)

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
            add_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric scores between 0 and 20.")

    confirm_button = ttk.Button(frame, text="Confirm", command=confirm, style="Accent.TButton")
    confirm_button.grid(row=6, column=1, columnspan=2, pady=10, sticky="ew")


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
    edit_window.configure(bg="#edd5e4")  #e3f2fd baby blue

    style = ttk.Style()
    style.configure("Custom.TFrame", background="#edd5e4")

    frame = ttk.Frame(edit_window, style="Custom.TFrame", padding=10)
    frame.pack(expand=True, fill="both")

    #labels and entry fields for scores
    ttk.Label(frame, text="Name:", background="#edd5e4").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = ttk.Entry(frame)
    name_entry.insert(0, student_data["name"])
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Math:", background="#edd5e4").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    math_entry = ttk.Entry(frame)
    math_entry.insert(0, student_data["math"])
    math_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Physique:",background="#edd5e4").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    physique_entry = ttk.Entry(frame)
    physique_entry.insert(0, student_data["physique"])
    physique_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Philosophie:",background="#edd5e4").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    philo_entry = ttk.Entry(frame)
    philo_entry.insert(0, student_data["philosophie"])
    philo_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="English:",background="#edd5e4").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    english_entry = ttk.Entry(frame)
    english_entry.insert(0, student_data["english"])
    english_entry.grid(row=4, column=1, padx=5, pady=5)

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
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=6)
    style.configure("Accent.TButton", background="#edd5e4",font=("Arial", 12, "bold"))
    style.map("Accent.TButton", background=[("active", "#e892e8")])
    ttk.Button(frame, text="Save Changes", style="Accent.TButton", command=save_changes).grid(
        row=5, column=1, columnspan=3, pady=10, padx=10, sticky="ew"
    )


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


def handle_export():
    filename = "students_export.csv"
    backend.export_to_csv(filename)
    messagebox.showinfo("Success", f"Student data exported to {filename}!")


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
    class_avg = backend.calculate_calss_average()
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


# Student Table
columns = ("Name", "Average", "Grade")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, width=150, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

tree.pack(fill="both", expand=True)

# Load students from CSV and display them in the table
backend.load_students()
update_student_list()

root.mainloop()
