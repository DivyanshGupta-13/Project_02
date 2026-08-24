import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, LabelFrame, Button, StringVar, RIDGE, W, BOTH, END
from PIL import Image, ImageTk
from db_helper import get_db_connection

class Student:
    def __init__(self, root):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.geometry("1530x780+0+0")
        try:
            self.root.attributes('-fullscreen', True)
        except Exception:
            pass

        self.root.title("Student Data")
        
        icon_path = os.path.join(self.base_dir, "face-id.ico")
        if os.path.exists(icon_path):
            try:
                self.root.wm_iconbitmap(icon_path)
            except Exception:
                pass

        # Variables
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_section = StringVar()
        self.var_std_name = StringVar()
        self.var_gender = StringVar()
        self.var_radio1 = StringVar()

        # Helper image loader
        def load_img(name, size):
            p = os.path.join(self.base_dir, "Images for face recognition project", name)
            if os.path.exists(p):
                img = Image.open(p).resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            return None

        # Top Header Images
        self.photoimg1 = load_img("img2.png", (500, 130))
        if self.photoimg1:
            Label(self.root, image=self.photoimg1).place(x=0, y=0, width=490, height=130)

        self.photoimg2 = load_img("img1.png", (500, 130))
        if self.photoimg2:
            Label(self.root, image=self.photoimg2).place(x=450, y=0, width=490, height=130)

        self.photoimg3 = load_img("img2.png", (500, 130))
        if self.photoimg3:
            Label(self.root, image=self.photoimg3).place(x=900, y=0, width=490, height=130)

        # Background image
        self.photoimg4 = load_img("bg_image.jpg", (1500, 680))
        bg_lbl = Label(self.root, image=self.photoimg4 if self.photoimg4 else None, bg="black")
        bg_lbl.place(x=0, y=130, width=1450, height=655)

        # Title label
        title_lbl = Label(bg_lbl, text="Student Details Management", font=("Georgia", 32, "bold"), bg="black", fg="Yellow")
        title_lbl.place(x=0, y=0, width=1360, height=50)

        # Back button
        B3 = Button(bg_lbl, text="Back", command=self.back, cursor="hand2", font=("Times New Roman", 16, "bold"), bg="Green", fg="white")
        B3.place(x=0, y=0, width=80, height=40)

        main_frame = Frame(bg_lbl, bd=5, bg="light blue")
        main_frame.place(x=20, y=70, width=1320, height=520)

        # Left label frame
        Left_frame = LabelFrame(main_frame, bd=3, bg="Light blue", relief=RIDGE, text="Student Details", font=("Georgia", 16, "bold"))
        Left_frame.place(x=10, y=10, width=650, height=480)

        # Academic frame
        Academic_frame = LabelFrame(Left_frame, bd=3, bg="Light blue", relief=RIDGE, text="Academic Information", font=("Georgia", 13))
        Academic_frame.place(x=5, y=5, width=630, height=140)

        # Course
        Label(Academic_frame, bd=1, bg="light blue", text="Course", font=("Times New Roman", 12)).grid(row=0, column=0, padx=5, pady=5)
        course_combo = ttk.Combobox(Academic_frame, textvariable=self.var_course, font=("Times New Roman", 12), state="readonly", width=15)
        course_combo["values"] = ("Select Course", "M-Tech", "B-Tech", "B-Pharma", "MBA", "BBA", "MCA", "BCA")
        course_combo.current(0)
        course_combo.grid(row=0, column=1, padx=5, pady=5)

        # Department
        Label(Academic_frame, bd=1, bg="light blue", text="Department", font=("Times New Roman", 12)).grid(row=0, column=2, padx=5, pady=5)
        Dept_combo = ttk.Combobox(Academic_frame, textvariable=self.var_dep, font=("Times New Roman", 12), state="readonly", width=15)
        Dept_combo["values"] = ("Select Department", "CSE", "Mechanical", "Electrical", "Electronics", "IT", "Not Applicable")
        Dept_combo.current(0)
        Dept_combo.grid(row=0, column=3, padx=5, pady=5)

        # Year
        Label(Academic_frame, bd=1, bg="light blue", text="Year", font=("Times New Roman", 12)).grid(row=1, column=0, padx=5, pady=5)
        year_combo = ttk.Combobox(Academic_frame, textvariable=self.var_year, font=("Times New Roman", 12), state="readonly", width=15)
        year_combo["values"] = ("Select Year", "1", "2", "3", "4")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=5, pady=5)

        # Semester
        Label(Academic_frame, bd=1, bg="light blue", text="Semester", font=("Times New Roman", 12)).grid(row=1, column=2, padx=5, pady=5)
        sem_combo = ttk.Combobox(Academic_frame, textvariable=self.var_semester, font=("Times New Roman", 12), state="readonly", width=15)
        sem_combo["values"] = ("Select Semester", "1", "2", "3", "4", "5", "6", "7", "8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=5, pady=5)

        # Class Information frame
        student_info = LabelFrame(Left_frame, bd=3, bg="Light blue", relief=RIDGE, text="Class & Student Information", font=("Georgia", 13))
        student_info.place(x=5, y=150, width=630, height=160)

        # Roll Number / Student ID
        Label(student_info, bd=1, bg="light blue", text="Roll Number", font=("Times New Roman", 12)).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(student_info, textvariable=self.var_std_id, width=15, font=("Georgia", 12)).grid(row=0, column=1, padx=5, pady=5)

        # Student Name
        Label(student_info, bd=1, bg="light blue", text="Student Name", font=("Times New Roman", 12)).grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(student_info, textvariable=self.var_std_name, width=18, font=("Georgia", 12)).grid(row=0, column=3, padx=5, pady=5)

        # Section
        Label(student_info, bd=1, bg="light blue", text="Section", font=("Times New Roman", 12)).grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(student_info, textvariable=self.var_section, width=15, font=("Georgia", 12)).grid(row=1, column=1, padx=5, pady=5)

        # Gender
        Label(student_info, bd=1, bg="light blue", text="Gender", font=("Times New Roman", 12)).grid(row=1, column=2, padx=5, pady=5)
        gender_combo = ttk.Combobox(student_info, textvariable=self.var_gender, font=("Times New Roman", 12), state="readonly", width=15)
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=1, column=3, padx=5, pady=5)

        # Radio buttons
        ttk.Radiobutton(student_info, text="Take Photo Sample", variable=self.var_radio1, value="Yes").grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        ttk.Radiobutton(student_info, text="No Photo Sample", variable=self.var_radio1, value="No").grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        # Buttons Frame
        btn_frame = Frame(Left_frame, bd=2, bg="light blue")
        btn_frame.place(x=5, y=320, width=630, height=40)

        Button(btn_frame, text="Save", command=self.add_data, width=14, font=("Times New Roman", 12, "bold"), bg="blue", fg="white").grid(row=0, column=0, padx=4)
        Button(btn_frame, text="Update", command=self.update_data, width=14, font=("Times New Roman", 12, "bold"), bg="blue", fg="white").grid(row=0, column=1, padx=4)
        Button(btn_frame, text="Delete", command=self.delete_data, width=14, font=("Times New Roman", 12, "bold"), bg="red", fg="white").grid(row=0, column=2, padx=4)
        Button(btn_frame, text="Reset", command=self.reset_data, width=14, font=("Times New Roman", 12, "bold"), bg="blue", fg="white").grid(row=0, column=3, padx=4)

        btn_frame1 = Frame(Left_frame, bd=2, bg="light blue")
        btn_frame1.place(x=5, y=370, width=630, height=45)

        Button(btn_frame1, text="Take Photo Sample (Register Face)", command=self.generate_dataset, width=45, font=("Times New Roman", 13, "bold"), bg="green", fg="white").pack(pady=5)

        # Right label frame - Student Table
        Right_frame = LabelFrame(main_frame, bd=3, bg="Light blue", relief=RIDGE, text="Student Table", font=("Georgia", 16, "bold"))
        Right_frame.place(x=670, y=10, width=630, height=480)

        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=10, width=615, height=430)

        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            column=("id", "name", "dep", "course", "section", "year", "sem", "gender", "photo"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("id", text="Roll Number")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("section", text="Section")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("photo", text="Photo Status")

        self.student_table["show"] = "headings"

        self.student_table.column("id", width=90)
        self.student_table.column("name", width=120)
        self.student_table.column("dep", width=90)
        self.student_table.column("course", width=80)
        self.student_table.column("section", width=60)
        self.student_table.column("year", width=60)
        self.student_table.column("sem", width=60)
        self.student_table.column("gender", width=70)
        self.student_table.column("photo", width=90)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    def add_data(self):
        if self.var_dep.get() in ("Select Department", "") or self.var_std_name.get().strip() == "" or self.var_std_id.get().strip() == "":
            messagebox.showerror("Error", "Roll Number, Name, and Department are required!", parent=self.root)
            return
        try:
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM student WHERE studentId=%s", (self.var_std_id.get().strip(),))
            if cur.fetchone() is not None:
                messagebox.showerror("Error", "Student with this Roll Number already exists!", parent=self.root)
                db.close()
                return

            cur.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                self.var_std_id.get().strip(),
                self.var_std_name.get().strip(),
                self.var_dep.get(),
                self.var_course.get(),
                self.var_section.get().strip(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_gender.get(),
                self.var_radio1.get()
            ))
            db.commit()
            db.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Student details added successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Database Error: {str(es)}", parent=self.root)

    def fetch_data(self):
        try:
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM student")
            data = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)
            db.close()
        except Exception as es:
            print("Fetch data error:", es)

    def get_cursor(self, event=""):
        try:
            cursor_focus = self.student_table.focus()
            content = self.student_table.item(cursor_focus)
            data = content.get("values", [])
            if data and len(data) >= 9:
                self.var_std_id.set(str(data[0]))
                self.var_std_name.set(str(data[1]))
                self.var_dep.set(str(data[2]))
                self.var_course.set(str(data[3]))
                self.var_section.set(str(data[4]))
                self.var_year.set(str(data[5]))
                self.var_semester.set(str(data[6]))
                self.var_gender.set(str(data[7]))
                self.var_radio1.set(str(data[8]))
        except Exception as e:
            print("get_cursor error:", e)

    def update_data(self):
        if self.var_std_id.get().strip() == "":
            messagebox.showerror("Error", "Roll Number is required to update!", parent=self.root)
            return
        try:
            if messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root):
                db = get_db_connection()
                cur = db.cursor()
                cur.execute("""
                UPDATE student SET studentName=%s, dep=%s, course=%s, section=%s, year=%s, sem=%s, gender=%s, photo=%s WHERE studentId=%s
                """, (
                    self.var_std_name.get().strip(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_section.get().strip(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_gender.get(),
                    self.var_radio1.get(),
                    self.var_std_id.get().strip()
                ))
                db.commit()
                db.close()
                self.fetch_data()
                messagebox.showinfo("Success", "Student details updated successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Database Error: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_std_id.get().strip() == "":
            messagebox.showerror("Error", "Roll Number required!", parent=self.root)
            return
        try:
            if messagebox.askyesno("Delete", "Do you want to delete this student and their face sample?", parent=self.root):
                std_id = self.var_std_id.get().strip()
                db = get_db_connection()
                cur = db.cursor()
                cur.execute("DELETE FROM student WHERE studentId=%s", (std_id,))
                db.commit()
                db.close()

                # Also delete face samples & update model
                from MAIN_CODE import FaceRecognitionSystem
                face_sys = FaceRecognitionSystem()
                face_sys.delete_user(std_id)

                self.fetch_data()
                self.reset_data()
                messagebox.showinfo("Success", "Student details and face data deleted successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Delete Error: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_section.set("")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_gender.set("Select Gender")
        self.var_radio1.set("")

    def generate_dataset(self):
        std_id = self.var_std_id.get().strip()
        if self.var_dep.get() in ("Select Department", "") or self.var_std_name.get().strip() == "" or std_id == "":
            messagebox.showerror("Error", "Roll Number, Name, and Department are required!", parent=self.root)
            return
        try:
            # Ensure student is saved in DB first
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM student WHERE studentId=%s", (std_id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    std_id,
                    self.var_std_name.get().strip(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_section.get().strip(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_gender.get(),
                    "Yes"
                ))
                db.commit()
            db.close()

            self.var_radio1.set("Yes")

            from MAIN_CODE import FaceRecognitionSystem
            face_sys = FaceRecognitionSystem()
            count = face_sys.register(std_id)

            self.fetch_data()
            messagebox.showinfo("Success", f"Captured {count} face samples and updated recognition model!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Dataset Generation Error: {str(es)}", parent=self.root)

    def back(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    obj = Student(root)
    root.mainloop()
