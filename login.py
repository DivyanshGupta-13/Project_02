import os
import tkinter as tk
from tkinter import ttk, messagebox, font, Toplevel, Label, Button, StringVar, Entry
from time import strftime
from PIL import Image, ImageTk
from db_helper import get_db_connection
from admin_login import Admin

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.title("Admin Login")
        self.root.geometry("650x650")
        self.root.configure(bg="black")

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

        self.photoimg4 = load_img("bg_image2.jpg", (1500, 800))
        bg_lbl = Label(self.root, image=self.photoimg4 if self.photoimg4 else None, bg="black")
        bg_lbl.place(x=0, y=0, width=1450, height=780)

        self.center_window()

        # Login Frame
        self.frame = tk.Frame(self.root, bg="black", bd=2, relief="ridge")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=380)

        self.title_label = tk.Label(self.frame, text="Admin Login", font=("Arial", 26, "bold"), fg="cyan", bg="black")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        self.username_label = tk.Label(self.frame, text="Username:", font=("Arial", 14), bg="black", fg="white")
        self.username_label.grid(row=1, column=0, sticky="w", padx=15, pady=10)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 14), bd=2, relief="solid", fg="black", width=22)
        self.username_entry.grid(row=1, column=1, padx=15, pady=10)

        # Password
        self.password_label = tk.Label(self.frame, text="Password:", font=("Arial", 14), bg="black", fg="white")
        self.password_label.grid(row=2, column=0, sticky="w", padx=15, pady=10)
        self.password_entry = tk.Entry(self.frame, font=("Arial", 14), bd=2, relief="solid", fg="black", width=22, show="*")
        self.password_entry.grid(row=2, column=1, padx=15, pady=10)

        # Login Button
        self.login_button = tk.Button(self.frame, text="Login", font=("Arial", 12, "bold"), fg="white", bg="green", bd=0,
                                      cursor="hand2", width=12, height=1, command=self.check_login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=15)

        # Forgot password button
        self.forgot_btn = tk.Button(self.frame, text="Forgot Password?", command=self.forgot, font=("Arial", 10, "underline"),
                                    fg="yellow", bg="black", bd=0, cursor="hand2")
        self.forgot_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # New registration button
        self.new_reg = tk.Button(self.frame, text="Register New Admin", font=("Arial", 10, "bold"),
                                 fg="cyan", bg="black", bd=0, cursor="hand2", command=self.registerwin)
        self.new_reg.grid(row=5, column=0, columnspan=2, pady=5)

        # Clock
        lbl = Label(bg_lbl, font=("calibri", 18, 'bold'), background='black', foreground='white')
        lbl.place(x=1150, y=20, height=35, width=200)

        def update_clock():
            lbl.config(text=strftime('%H:%M:%S %p'))
            lbl.after(1000, update_clock)

        update_clock()

    def center_window(self):
        window_width = 550
        window_height = 550
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = max(0, int(screen_height / 2 - window_height / 2))
        position_right = max(0, int(screen_width / 2 - window_width / 2))
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def registerwin(self):
        new_window = Toplevel(self.root)
        self.reg_app = RegistrationForm(new_window)

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        try:
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM register WHERE username=%s AND pass=%s", (username, password))
            row = cur.fetchone()
            db.close()

            if row is None:
                messagebox.showerror("Login Failed", "Incorrect Username or Password", parent=self.root)
            else:
                messagebox.showinfo("Login Success", "Welcome, Admin!", parent=self.root)
                self.root.destroy()
                admin_root = tk.Tk()
                Admin(admin_root)
                admin_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.root)

    def forgot(self):
        username = self.username_entry.get().strip()
        if username == "":
            messagebox.showerror("Error", "Please enter your username in the login form first!", parent=self.root)
            return

        try:
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT security, ans FROM register WHERE username=%s", (username,))
            row = cur.fetchone()
            db.close()

            if row is None:
                messagebox.showerror("Error", "Username does not exist!", parent=self.root)
                return

            self.forgot_user = username
            self.db_security = row[0]
            self.db_ans = row[1]

            self.root2 = Toplevel(self.root)
            self.root2.title("Reset Password")
            self.root2.geometry("500x300+450+250")
            self.root2.configure(bg="black")

            Label(self.root2, text=f"Security Verification for: {username}", font=("Times New Roman", 16, "bold"), bg="black", fg="yellow").place(x=0, y=15, relwidth=1)

            Label(self.root2, text="Security Question:", font=("Times New Roman", 12), bg="black", fg="white").place(x=20, y=70)
            self.sec_lbl = Label(self.root2, text=self.db_security, font=("Times New Roman", 12, "italic"), bg="black", fg="cyan", wraplength=450, justify="left")
            self.sec_lbl.place(x=20, y=100)

            Label(self.root2, text="Your Answer:", font=("Times New Roman", 12), bg="black", fg="white").place(x=20, y=150)
            self.entry_ans1 = Entry(self.root2, font=("Times New Roman", 12), bd=2, width=30)
            self.entry_ans1.place(x=150, y=150)

            Button(self.root2, text="Verify Answer", command=self.validate_forgot, font=("Times New Roman", 12, "bold"), bg="green", fg="white", cursor="hand2").place(x=180, y=210)
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving user: {str(e)}", parent=self.root)

    def validate_forgot(self):
        user_ans = self.entry_ans1.get().strip()
        if user_ans == "":
            messagebox.showerror("Error", "Please enter your answer!", parent=self.root2)
            return

        if user_ans.lower() == str(self.db_ans).strip().lower():
            messagebox.showinfo("Success", "Security check verified! Opening Admin Dashboard...", parent=self.root2)
            self.root2.destroy()
            self.root.destroy()
            admin_root = tk.Tk()
            Admin(admin_root)
            admin_root.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect answer! Access denied.", parent=self.root2)


class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.title("Admin Registration")
        self.root.geometry("1530x780+0+0")
        try:
            self.root.attributes('-fullscreen', True)
        except Exception:
            pass

        def load_img(name, size):
            p = os.path.join(self.base_dir, "Images for face recognition project", name)
            if os.path.exists(p):
                img = Image.open(p).resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            return None

        self.photoimg4 = load_img("bg_image.jpg", (1500, 720))
        bg_lbl = Label(self.root, image=self.photoimg4 if self.photoimg4 else None, bg="black")
        bg_lbl.place(x=0, y=0, width=1480, height=720)

        title_lbl = Label(bg_lbl, text="Admin Account Registration", font=("Times New Roman", 28, "bold"), bg="black", fg="yellow")
        title_lbl.place(x=0, y=0, width=1360, height=50)

        self.var_name = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()
        self.var_security = StringVar()
        self.var_ans = StringVar()

        self.frame = tk.Frame(self.root, bg="black", padx=30, pady=30, bd=2, relief="ridge")
        self.frame.pack(padx=10, pady=80)

        custom_font = ("Helvetica", 13)

        Label(self.frame, text="Username:", font=custom_font, bg="black", fg="white").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        Entry(self.frame, textvariable=self.var_name, font=custom_font, bd=2, width=30).grid(row=0, column=1, pady=10, padx=10)

        Label(self.frame, text="Enter Password:", font=custom_font, bg="black", fg="white").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        Entry(self.frame, textvariable=self.var_pass, font=custom_font, bd=2, show="*", width=30).grid(row=1, column=1, pady=10, padx=10)

        Label(self.frame, text="Confirm Password:", font=custom_font, bg="black", fg="white").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        Entry(self.frame, textvariable=self.var_confpass, font=custom_font, bd=2, show="*", width=30).grid(row=2, column=1, pady=10, padx=10)

        Label(self.frame, text="Security Question:", font=custom_font, bg="black", fg="white").grid(row=3, column=0, pady=10, padx=10, sticky="w")
        security_combo = ttk.Combobox(self.frame, textvariable=self.var_security, font=custom_font, state="readonly", width=28)
        security_combo["values"] = ("Select Question", "In which city did you born?", "What is name of your first school?", "What is your favorite color?")
        security_combo.current(0)
        security_combo.grid(row=3, column=1, padx=10, pady=10)

        Label(self.frame, text="Enter Answer:", font=custom_font, bg="black", fg="white").grid(row=4, column=0, pady=10, padx=10, sticky="w")
        Entry(self.frame, textvariable=self.var_ans, font=custom_font, bd=2, width=30).grid(row=4, column=1, pady=10, padx=10)

        Button(self.frame, text="Register Now", command=self.register_user, font=("Helvetica", 13, "bold"), bg="#4CAF50", fg="white", bd=0, width=20, height=2, cursor="hand2").grid(row=5, column=0, columnspan=2, pady=20)
        Button(self.frame, text="Close", command=self.root.destroy, font=("Helvetica", 11), bg="red", fg="white", cursor="hand2").grid(row=6, column=0, columnspan=2)

    def register_user(self):
        uname = self.var_name.get().strip()
        pwd = self.var_pass.get().strip()
        cpwd = self.var_confpass.get().strip()
        sec = self.var_security.get()
        ans = self.var_ans.get().strip()

        if uname == "" or pwd == "" or cpwd == "" or sec == "Select Question" or ans == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        if pwd != cpwd:
            messagebox.showerror("Error", "Password and Confirm Password do not match!", parent=self.root)
            return

        try:
            db = get_db_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM register WHERE username=%s", (uname,))
            if cur.fetchone() is not None:
                messagebox.showerror("Alert", "Username already exists! Please choose another.", parent=self.root)
                db.close()
                return

            cur.execute("INSERT INTO register VALUES (%s, %s, %s, %s, %s)", (uname, pwd, cpwd, sec, ans))
            db.commit()
            db.close()

            messagebox.showinfo("Success", f"Registration Successful!\nUsername: {uname}", parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Registration Failed: {str(e)}", parent=self.root)

def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
