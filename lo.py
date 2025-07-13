
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import json
from datetime import datetime
import requests
import pyttsx3
import string

#{------------TTS Setup------------------------}

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 160)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

def init_data_files():
    for file in ['users.txt', 'feedback.txt']:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('')

def send_to_discord(feedback_data):
    content = (
        f"\n📣 **New Feedback Submitted**\n"
        f"🧑 User: {feedback_data['username']}\n"
        f"📝 Subject: {feedback_data['subject']}\n"
        f"📂 Category: {feedback_data['category']}\n"
        f"📃 Description: {feedback_data['description']}\n"
        f"🖼 Image: {feedback_data['image'] if feedback_data['image'] else 'No Image'}\n"
        f"🕒 Date: {feedback_data['date']}"
    )
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
    except Exception as e:
        print("Discord Error:", e)

#{------------------------code for placeholder-------------------------}



def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(show="*" if placeholder == "Password" else "", fg="black")

def add_placeholder(event, entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)
        entry.config(show="" if placeholder == "Username" else "*", fg="gray")

#{---------------------------code for login windwo(window-1)---------------------}


def show_login_window():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("800x500")
    login_window.configure(bg="#1a1a3d")

#[--------------------- code for left side-------------- ]


    left_frame = tk.Frame(login_window, bg="#1a1a3d", width=350, height=500)
    left_frame.pack(side="left", fill="y")

    tk.Label(left_frame, text="👤", font=("Arial", 50), bg="#1a1a3d", fg="white").place(x=130, y=80)


#[----------------------code for username and password field----------------]


    username_entry = tk.Entry(left_frame, font=("Arial", 14), fg="gray")
    username_entry.insert(0, "Username")
    username_entry.bind("<FocusIn>", lambda e: clear_placeholder(e, username_entry, "Username"))
    username_entry.bind("<FocusOut>", lambda e: add_placeholder(e, username_entry, "Username"))
    username_entry.place(x=70, y=170, width=200, height=30)

    password_entry = tk.Entry(left_frame, font=("Arial", 14), fg="gray")
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", lambda e: clear_placeholder(e, password_entry, "Password"))
    password_entry.bind("<FocusOut>", lambda e: add_placeholder(e, password_entry, "Password"))
    password_entry.place(x=70, y=220, width=200, height=30)

#{------------------------code for login condition-------------------}



    def login():
        username = username_entry.get()
        password = password_entry.get()
        with open('users.txt', 'r') as f:
            for line in f:
                u, p, t = line.strip().split(',')
                if u == username and p == password:
                    login_window.destroy()
                    show_main_window(username, t)
                    return
        speak("Invalid credentials!")
        messagebox.showerror("Login Failed", "Invalid credentials!")
 
    tk.Button(left_frame, text="Login", font=("Arial", 12, "bold"), bg="#ff007f", fg="white", command=login).place(x=110, y=270, width=120, height=35)
    tk.Button(left_frame, text="Sign Up", font=("Arial", 12, "bold"), bg="#ff007f", fg="white", command=lambda: [login_window.destroy(), show_signup_window()]).place(x=110, y=320, width=120, height=35)
 

#{----------------code for right side frame-----------------------------} 

    right_frame = tk.Frame(login_window, width=450, height=500)
    right_frame.pack(side="right", fill="both")

#[............code for image.............]

    if os.path.exists("log.png"):
        img = Image.open("log.png").resize((450, 500))
        bg_photo = ImageTk.PhotoImage(img)
        tk.Label(right_frame, image=bg_photo).place(relwidth=1, relheight=1)
        right_frame.image = bg_photo

    tk.Label(right_frame, text="Welcome.", font=("Arial", 32, "bold"), bg="black", fg="white").place(x=100, y=150)
    tk.Label(right_frame, text="Enter username and password on the left to login.", font=("Arial", 12),
             bg="black", fg="white", justify="left").place(x=80, y=210)

    login_window.mainloop()
#{--------------code for signup window(window-2)------------------}



def show_signup_window():
    signup_window = tk.Tk()
    signup_window.title("Sign Up")
    signup_window.geometry("800x500")
    signup_window.configure(bg="#335975")
#[........ code for left side frame...............]


    left_frame = tk.Frame(signup_window, bg="#335975", width=350, height=500)
    left_frame.pack(side="left", fill="y")

    tk.Label(left_frame, text="👤", font=("Arial", 50), bg="#335975", fg="white").place(x=130, y=80)
#[..............code for niput filde of singup..............]



    username_entry = tk.Entry(left_frame, font=("Arial", 14), fg="gray")
    username_entry.insert(0, "Username")
    username_entry.bind("<FocusIn>", lambda e: clear_placeholder(e, username_entry, "Username"))
    username_entry.bind("<FocusOut>", lambda e: add_placeholder(e, username_entry, "Username"))
    username_entry.place(x=70, y=170, width=200, height=30)

    password_entry = tk.Entry(left_frame, font=("Arial", 14), fg="gray")
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", lambda e: clear_placeholder(e, password_entry, "Password"))
    password_entry.bind("<FocusOut>", lambda e: add_placeholder(e, password_entry, "Password"))
    password_entry.place(x=70, y=220, width=200, height=30)

    tk.Label(left_frame, text="User Type:", bg="#335975", fg="white").place(x=70, y=270)
    user_type = tk.StringVar(value="user")
    ttk.Radiobutton(left_frame, text="User", variable=user_type, value="user").place(x=70, y=300)
    ttk.Radiobutton(left_frame, text="Admin", variable=user_type, value="admin").place(x=150, y=300)
 
#[..............code for signup condition..........]


    def signup():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            speak("All fields are required!")
            messagebox.showerror("Error", "All fields are required!")
            return

        if len(password) < 8 or not any(char in string.punctuation for char in password):
            speak("Password must be at least 8 characters long and include a special character.")
            messagebox.showerror("Error", "Weak password!")
            return

        with open('users.txt', 'r') as f:
            for line in f:
                if username == line.strip().split(',')[0]:
                    speak("Username already exists!")
                    messagebox.showerror("Error", "Username already exists!")
                    return

        with open('users.txt', 'a') as f:
            f.write(f"{username},{password},{user_type.get()}\n")

        speak("Account created successfully!")
        messagebox.showinfo("Success", "Account created successfully!")
        signup_window.destroy()
        show_login_window()

    tk.Button(left_frame, text="Sign Up", command=signup).place(x=110, y=360, width=120, height=35)
    tk.Button(left_frame, text="Back to Login", command=lambda: [signup_window.destroy(), show_login_window()]).place(x=110, y=410, width=120, height=35)
#[..................right side frame..........]


    right_frame = tk.Frame(signup_window, width=450, height=500)
    right_frame.pack(side="right", fill="both")
#[...........code for image............]


    if os.path.exists("si.jpg"):
        img = Image.open("si.jpg").resize((450, 500))
        bg_photo = ImageTk.PhotoImage(img)
        tk.Label(right_frame, image=bg_photo).place(relwidth=1, relheight=1)
        right_frame.image = bg_photo

    tk.Label(right_frame, text="Welcome.", font=("Arial", 32, "bold"), bg="black", fg="white").place(x=100, y=150)
    tk.Label(right_frame, text="Enter username and password on the left to signup.", font=("Arial", 12),
             bg="black", fg="white", justify="left").place(x=80, y=210)

    signup_window.mainloop()
  

#{-------------------code for feedback system--------------------------}


def show_main_window(username, user_type):
    main = tk.Tk()
    main.title(f"Feedback System - {username}")
    main.geometry("1200x600")
    main.configure(bg="white")

    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Helvetica', 12, 'bold'))
    style.configure('TButton', font=('Helvetica', 12))

    
    left_frame = tk.Frame(main,relief=tk.RIDGE, bg='white')
    left_frame.place(x=0,y=0,width=500,height=600)
    try:
        img = Image.open("im.jpg")
        img = img.resize((350, 400))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(left_frame, image=photo, bg='white')
        label.image = photo
        label.pack()
    except:
        label = tk.Label(left_frame, text="Image not found", bg='white', font=("Arial", 14))
        label.pack()

    right_frame = tk.Frame(main,relief=tk.RIDGE,bg='white')
    right_frame.place(x=500,y=0,width=700,height=600)
    
#[.............code for Creating notebook.............]
    

    notebook = ttk.Notebook(right_frame)
    notebook.pack(fill="both", expand=True)

    submit_frame = tk.Frame(notebook, bg='white')
    view_frame = tk.Frame(notebook, bg='white')
    notebook.add(submit_frame, text="Submit Feedback")
    notebook.add(view_frame, text="View Feedback")

    tk.Label(submit_frame, text="Product Name:", font=("Arial", 14), bg="white").pack(pady=5)
    subject_entry = tk.Entry(submit_frame,bg="lightgray", font=("Arial", 12), width=30)
    subject_entry.pack()

    tk.Label(submit_frame, text="Category:", font=("Arial", 14), bg="white").pack(pady=5)
    category_var = tk.StringVar(value="General")
    category_menu = ttk.Combobox(submit_frame, textvariable=category_var,
                                 values=["General", "Technical", "Product", "Service", "Other"], font=("Arial", 12))
    category_menu.pack()

    tk.Label(submit_frame, text="Description:", font=("Arial", 14), bg="white").pack(pady=10)
    description_text = tk.Text(submit_frame, bg="lightgray",height=5, width=60, font=("Arial", 12))
    description_text.pack()

    image_var = tk.StringVar()
    image_entry = tk.Entry(submit_frame, textvariable=image_var, font=("Arial", 10), state='readonly', width=50)
    image_entry.pack(pady=5)
    tk.Button(submit_frame, text="Browse Image", width=10,bg="#A7CDCB",command=lambda: image_var.set(
        filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg *.jpeg *.gif")]))).pack(pady=5)

#[............code for submit feedback............]


 
    def submit_feedback():
        feedback = {
            "id": f"FB{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "username": username,
            "subject": subject_entry.get(),
            "category": category_var.get(),
            "description": description_text.get("1.0", "end").strip(),
            "status": "Pending",
            "response": "",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image": image_var.get()
        }

        if not all([feedback['subject'], feedback['category'], feedback['description']]):
            speak("All fields except image are required!")
            messagebox.showerror("Error", "All fields except image are required!")
            return

        with open('feedback.txt', 'a') as f:
            f.write(json.dumps(feedback) + '\n')

        send_to_discord(feedback)
        speak("Feedback submitted successfully!")
        messagebox.showinfo("Success", f"Feedback submitted! ID: {feedback['id']}")
        subject_entry.delete(0, tk.END)
        description_text.delete("1.0", tk.END)
        image_var.set("")
        refresh_tree()

    tk.Button(submit_frame, text="Submit",width=20,bg="#A7CDCB", font=("Arial", 16), command=submit_feedback).pack(pady=10)

    tree = ttk.Treeview(view_frame, columns=('ID', 'subject', 'category', 'status', 'response'), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col.title())
    tree.pack(expand=True, fill="both")

    def refresh_tree():
        tree.delete(*tree.get_children())
        with open("feedback.txt", "r") as f:
            for line in f:
                fb = json.loads(line)
                if user_type == "admin" or fb["username"] == username:
                    tree.insert("", "end", values=(fb["id"], fb["subject"], fb["category"], fb["status"], fb["response"]))

#[............code for Creating response entry................] 

    



    if user_type == "admin":
        response_entry = tk.Entry(view_frame, width=40,bg="lightgray")
        response_entry.pack(pady=5)
        status_var = tk.StringVar(value="Pending")
        ttk.Combobox(view_frame, textvariable=status_var, values=["Pending", "In Progress", "Resolved"]).pack()

        def update_feedback():
            selected = tree.selection()
            if not selected:
                speak("No feedback selected")
                messagebox.showerror("Error", "No feedback selected")
                return
            feedback_id = tree.item(selected)["values"][0]
            new_response = response_entry.get()
            new_status = status_var.get()
            lines = []
            with open("feedback.txt", "r") as f:
                for line in f:
                    fb = json.loads(line)
                    if fb["id"] == feedback_id:
                        fb["response"] = new_response
                        fb["status"] = new_status
                    lines.append(json.dumps(fb) + '\n')
            with open("feedback.txt", "w") as f:
                f.writelines(lines)
            refresh_tree()
            response_entry.delete(0, tk.END)
#[............code for view freme button..............]




        tk.Button(view_frame, text="Update Feedback", width=20,bg="#8D9FCD",command=update_feedback).pack(pady=5)

    tk.Button(view_frame, text="Refresh", font=("Arial", 15), bg="#8D9FCD",width=30, command=refresh_tree).pack(pady=5)
    tk.Button(view_frame, text="Open Image", font=("Arial", 15), bg="#8D9FCD",width=30, command=lambda: os.startfile(
        next((json.loads(line)["image"] for line in open("feedback.txt") if tree.selection() and json.loads(line)["id"] == tree.item(tree.selection())["values"][0]), "")
    ) if tree.selection() else speak("Please select a feedback") or messagebox.showerror("No selection", "Please select a feedback")).pack(pady=5)

    refresh_tree()
    main.mainloop()

def main():
    init_data_files()
    show_login_window()

if __name__ == "__main__":
    main()
