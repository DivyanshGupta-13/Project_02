import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Frame, Label, LabelFrame, Button, StringVar, RIDGE, W, BOTH, END
from PIL import Image, ImageTk

class Attendence:
    def __init__(self, root):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.geometry("1530x780+0+0")
        try:
            self.root.attributes('-fullscreen', True)
        except Exception:
            pass

        self.root.title("Attendance Records")
        
        icon_path = os.path.join(self.base_dir, "face-id.ico")
        if os.path.exists(icon_path):
            try:
                self.root.wm_iconbitmap(icon_path)
            except Exception:
                pass

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_dep = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_status = StringVar()

        self.mydata = []

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
        title_lbl = Label(bg_lbl, text="Attendance Log & Reports", font=("Georgia", 32, "bold"), bg="black", fg="chartreuse")
        title_lbl.place(x=0, y=0, width=1360, height=50)

        main_frame = Frame(bg_lbl, bd=5, bg="orange2")
        main_frame.place(x=20, y=70, width=1320, height=520)

        # Back button
        B3 = Button(bg_lbl, text="Back", command=self.back, cursor="hand2", font=("Times New Roman", 16, "bold"), bg="Green", fg="white")
        B3.place(x=0, y=0, width=80, height=40)

        # Left Frame - Form details
        Left_frame = LabelFrame(main_frame, bd=3, bg="Light blue", relief=RIDGE, text="Selected Attendance Details", font=("Georgia", 16, "bold"))
        Left_frame.place(x=10, y=10, width=650, height=480)

        left_inside_frame = LabelFrame(Left_frame, bd=3, bg="Light blue", relief=RIDGE)
        left_inside_frame.place(x=5, y=10, width=635, height=380)

        # Roll Number
        Label(left_inside_frame, bd=1, bg="light blue", text="Roll Number: ", font=("Times New Roman", 12)).grid(row=0, column=0, padx=8, pady=10, sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_roll, width=16, font=("Georgia", 12)).grid(row=0, column=1, padx=8)

        # Name
        Label(left_inside_frame, bd=1, bg="light blue", text="Name: ", font=("Times New Roman", 12)).grid(row=0, column=2, padx=8, pady=10, sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_name, width=16, font=("Georgia", 12)).grid(row=0, column=3, padx=8)

        # Department
        Label(left_inside_frame, bd=1, bg="light blue", text="Department: ", font=("Times New Roman", 12)).grid(row=1, column=0, padx=8, pady=10, sticky=W)
        Dep_combo = ttk.Combobox(left_inside_frame, font=("Times New Roman", 12), textvariable=self.var_dep, state="readonly", width=14)
        Dep_combo["values"] = ("Select Department", "CSE", "Mechanical", "Electrical", "Electronics", "IT", "Not Applicable")
        Dep_combo.current(0)
        Dep_combo.grid(row=1, column=1, padx=8, pady=10, sticky=W)

        # Time
        Label(left_inside_frame, bd=1, bg="light blue", text="Time: ", font=("Times New Roman", 12)).grid(row=1, column=2, padx=8, pady=10, sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_time, width=16, font=("Georgia", 12)).grid(row=1, column=3, padx=8)

        # Date
        Label(left_inside_frame, bd=1, bg="light blue", text="Date: ", font=("Times New Roman", 12)).grid(row=2, column=0, padx=8, pady=10, sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_date, width=16, font=("Georgia", 12)).grid(row=2, column=1, padx=8)

        # Status
        Label(left_inside_frame, bd=1, bg="light blue", text="Status: ", font=("Times New Roman", 12)).grid(row=2, column=2, padx=8, pady=10, sticky=W)
        att_combo = ttk.Combobox(left_inside_frame, textvariable=self.var_status, font=("Times New Roman", 12), state="readonly", width=14)
        att_combo["values"] = ("Select Status", "Present", "Absent")
        att_combo.current(0)
        att_combo.grid(row=2, column=3, padx=8, pady=10, sticky=W)

        # Action Buttons Frame
        btn_frame = Frame(left_inside_frame, bd=2, bg="light blue")
        btn_frame.place(x=5, y=300, width=620, height=45)

        Button(btn_frame, text="Import CSV", command=self.import_csv, width=18, font=("Times New Roman", 12, "bold"), bg="blue", fg="white").grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Export CSV", command=self.export_csv, width=18, font=("Times New Roman", 12, "bold"), bg="blue", fg="white").grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Reset", command=self.reset_data, width=18, font=("Times New Roman", 12, "bold"), bg="blue", fg="white").grid(row=0, column=2, padx=5)

        # Right Frame - Attendance Table
        Right_frame = LabelFrame(main_frame, bd=3, bg="Light blue", relief=RIDGE, text="Attendance Table", font=("Georgia", 16, "bold"))
        Right_frame.place(x=670, y=10, width=630, height=480)

        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=5, width=615, height=430)

        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.attendence_table = ttk.Treeview(
            table_frame,
            column=("Roll", "name", "dep", "time", "date", "status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.attendence_table.xview)
        scroll_y.config(command=self.attendence_table.yview)

        self.attendence_table.heading("Roll", text="Roll Number")
        self.attendence_table.heading("name", text="Name")
        self.attendence_table.heading("dep", text="Department")
        self.attendence_table.heading("time", text="Time")
        self.attendence_table.heading("date", text="Date")
        self.attendence_table.heading("status", text="Status")

        self.attendence_table["show"] = "headings"

        self.attendence_table.column("Roll", width=100)
        self.attendence_table.column("name", width=120)
        self.attendence_table.column("dep", width=100)
        self.attendence_table.column("time", width=90)
        self.attendence_table.column("date", width=90)
        self.attendence_table.column("status", width=80)

        self.attendence_table.pack(fill=BOTH, expand=1)
        self.attendence_table.bind("<ButtonRelease>", self.get_cursor)

        # Automatically load current attendance records on open
        self.auto_load_attendance()

    def auto_load_attendance(self):
        csv_path = os.path.join(self.base_dir, "Attendence folder", "ATTENDANCE.csv")
        if os.path.exists(csv_path):
            try:
                self.mydata.clear()
                with open(csv_path, "r", encoding="utf-8") as f:
                    csvread = csv.reader(f)
                    for i, row in enumerate(csvread):
                        if i == 0 and len(row) > 0 and row[0].lower() in ("roll", "roll number", "std"):
                            continue # Skip header
                        if len(row) >= 6:
                            self.mydata.append(row[:6])
                self.fetch_data(self.mydata)
            except Exception as e:
                print("Auto load error:", e)

    def fetch_data(self, rows):
        self.attendence_table.delete(*self.attendence_table.get_children())
        for row in rows:
            if len(row) >= 6:
                self.attendence_table.insert("", END, values=row)

    def import_csv(self):
        filename = filedialog.askopenfilename(
            initialdir=self.base_dir,
            title="Open Attendance CSV",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
            parent=self.root
        )
        if not filename:
            return

        try:
            self.mydata.clear()
            with open(filename, "r", encoding="utf-8") as myfile:
                csvread = csv.reader(myfile)
                for i, row in enumerate(csvread):
                    if i == 0 and len(row) > 0 and row[0].lower() in ("roll", "roll number", "std"):
                        continue
                    if len(row) >= 6:
                        self.mydata.append(row[:6])
            self.fetch_data(self.mydata)
            messagebox.showinfo("Imported", f"Successfully loaded {len(self.mydata)} records from {os.path.basename(filename)}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Could not read CSV file: {str(es)}", parent=self.root)

    def export_csv(self):
        if len(self.mydata) < 1:
            messagebox.showerror("No Data", "No data available to export!", parent=self.root)
            return

        filename = filedialog.asksaveasfilename(
            initialdir=self.base_dir,
            title="Export Attendance CSV",
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
            parent=self.root
        )
        if not filename:
            return

        try:
            with open(filename, mode='w', newline="", encoding="utf-8") as myfile:
                exp_write = csv.writer(myfile)
                exp_write.writerow(["Roll", "Name", "Department", "Time", "Date", "Status"])
                for i in self.mydata:
                    exp_write.writerow(i)
            messagebox.showinfo("Success", f"Attendance data exported to {os.path.basename(filename)} successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Could not export CSV: {str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        try:
            cursor_row = self.attendence_table.focus()
            content = self.attendence_table.item(cursor_row)
            rows = content.get('values', [])
            if rows and len(rows) >= 6:
                self.var_roll.set(str(rows[0]))
                self.var_name.set(str(rows[1]))
                self.var_dep.set(str(rows[2]))
                self.var_time.set(str(rows[3]))
                self.var_date.set(str(rows[4]))
                self.var_status.set(str(rows[5]))
        except Exception as e:
            print("get_cursor error:", e)

    def reset_data(self):
        self.var_name.set("")
        self.var_roll.set("")
        self.var_dep.set("Select Department")
        self.var_time.set("")
        self.var_date.set("")
        self.var_status.set("Select Status")

    def back(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    obj = Attendence(root)
    root.mainloop()
