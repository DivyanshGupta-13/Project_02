import os
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button
from time import strftime
from PIL import Image, ImageTk

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.geometry("1530x780+0+0")
        try:
            self.root.attributes('-fullscreen', True)
        except Exception:
            pass

        self.root.title("Face Recognition Attendance System")
        
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
        title_lbl = Label(bg_lbl, text="FACE RECOGNITION BASED ATTENDANCE SYSTEM", font=("Georgia", 32, "bold"), bg="black", fg="Yellow")
        title_lbl.place(x=0, y=0, width=1360, height=50)

        # Mark Attendance Button
        B1 = Button(bg_lbl, text="Mark Attendance\n(Start Camera)", cursor="hand2", command=self.mark_attendance, font=("Times New Roman", 18, "bold"), bg="Orange", fg="Blue")
        B1.place(x=400, y=250, width=220, height=120)

        # Admin Login Button
        B2 = Button(bg_lbl, text="Login as Admin", command=self.login, cursor="hand2", font=("Times New Roman", 18, "bold"), bg="Orange", fg="Blue")
        B2.place(x=720, y=250, width=220, height=120)

        # Exit Button
        B3 = Button(bg_lbl, text="Exit System", command=self.exit_app, cursor="hand2", font=("Times New Roman", 16, "bold"), bg="Red", fg="white")
        B3.place(x=20, y=580, width=140, height=50)

        # Date / Clock Labels
        lbl_time = Label(bg_lbl, font=("calibri", 18, "bold"), background='black', foreground='white')
        lbl_date = Label(bg_lbl, font=("calibri", 18, "bold"), background='black', foreground='white')
        lbl_day = Label(bg_lbl, font=("calibri", 18, "bold"), background='black', foreground='white')

        lbl_time.place(x=1140, y=500, height=30, width=200)
        lbl_date.place(x=1140, y=535, height=30, width=200)
        lbl_day.place(x=1140, y=570, height=30, width=200)

        def update_clock():
            lbl_time.config(text=strftime('%H:%M:%S %p'))
            lbl_date.config(text=strftime("%d/%m/%Y"))
            lbl_day.config(text=strftime("%A"))
            lbl_time.after(1000, update_clock)

        update_clock()

    def mark_attendance(self):
        try:
            from MAIN_CODE import FaceRecognitionSystem
            face_sys = FaceRecognitionSystem()
            face_sys.attendance()
        except Exception as e:
            messagebox.showerror("Error", f"Could not start face recognition camera:\n{str(e)}", parent=self.root)

    def login(self):
        popup = Toplevel(self.root)
        from login import LoginApp
        LoginApp(popup)

    def exit_app(self):
        if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
