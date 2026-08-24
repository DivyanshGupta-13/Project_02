import os
import sys
import subprocess
import tkinter as tk
from tkinter import Toplevel, Label, Button
from time import strftime
from PIL import Image, ImageTk
from student import Student
from attendance import Attendence

class Admin:
    def __init__(self, root):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.geometry("1530x780+0+0")
        try:
            self.root.attributes('-fullscreen', True)
        except Exception:
            pass

        self.root.title("Admin Dashboard")
        
        icon_path = os.path.join(self.base_dir, "face-id.ico")
        if os.path.exists(icon_path):
            try:
                self.root.wm_iconbitmap(icon_path)
            except Exception:
                pass

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
        title_lbl = Label(bg_lbl, text="Admin Control Panel", font=("Georgia", 36, "bold"), bg="black", fg="Yellow")
        title_lbl.place(x=0, y=0, width=1360, height=50)

        # Navigation Buttons
        B1 = Button(bg_lbl, text="Student Details", command=self.student_details, cursor="hand2", font=("Times New Roman", 18, "bold"), bg="Orange", fg="white")
        B1.place(x=280, y=250, width=200, height=80)

        B2 = Button(bg_lbl, text="Attendance Log", command=self.attendence, cursor="hand2", font=("Times New Roman", 18, "bold"), bg="Orange", fg="white")
        B2.place(x=580, y=250, width=200, height=80)

        B3 = Button(bg_lbl, text="Face Samples", command=self.open_image, cursor="hand2", font=("Times New Roman", 18, "bold"), bg="Orange", fg="white")
        B3.place(x=880, y=250, width=200, height=80)

        # Back button
        B_back = Button(bg_lbl, text="Back", command=self.back, cursor="hand2", font=("Times New Roman", 18, "bold"), bg="Green", fg="white")
        B_back.place(x=0, y=0, width=80, height=40)

        # Clock
        lbl_clock = Label(bg_lbl, font=("calibri", 22, 'bold'), background='black', foreground='white')
        lbl_clock.place(x=1140, y=560, height=40, width=210)

        def update_time():
            time_str = strftime('%H:%M:%S %p')
            lbl_clock.config(text=time_str)
            lbl_clock.after(1000, update_time)

        update_time()

    def back(self):
        self.root.destroy()

    def open_image(self):
        folder_path = os.path.join(self.base_dir, "ACTUAL_DATA")
        os.makedirs(folder_path, exist_ok=True)
        try:
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as e:
            print("Folder open error:", e)

    def student_details(self):
        new_window = Toplevel(self.root)
        self.student_win = Student(new_window)

    def attendence(self):
        new_window = Toplevel(self.root)
        self.att_win = Attendence(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    obj = Admin(root)
    root.mainloop()
