import tkinter as tk
from tkinter import messagebox
import mysql.connector
conn=mysql.connector.connect(host='localhost',username='root',password='sadneya@sam05',database='Ehealthcare')
cursor=conn.cursor()
print(conn)
#create database Ehealthcare;
'''create a table'''
# cursor.execute("create table doctor(id int primary key auto_increment,first_name varchar(255),last_name varchar(255),email varchar(255),phoneNo varchar(255),password varchar(255),qualifiaction varchar(255),rating varchar(255))")
# cursor.execute("create table admin(id int,first_name varchar(255),last_name varchar(255),email varchar(255) primary key,password varchar(255))")
import tkinter as tk
from tkinter import messagebox
import mysql.connector

def view_profile():
    email = email_entry.get()
    password = password_entry.get()
    cursor.execute("select * from doctor where email=%s and password=%s", (email, password))
    result = cursor.fetchone()
    if result:
        profile_text.delete(1.0, tk.END)
        profile_text.insert(tk.END, f"First Name: {result[1]}\nLast Name: {result[2]}\nEmail: {result[3]}\nPhone numebr:{result[4]}\nQualification:{result[5]}")
    else:
        messagebox.showerror("Error", "Invalid credentials")

def register():
    # id_val = id_entry.get()
    first_name_val = first_name_entry.get()
    last_name_val = last_name_entry.get()
    email_val = email_entry_reg.get()
    password_val = password_entry_reg.get()
    qualification_val = qualification_entry.get()

    val = (first_name_val, last_name_val, email_val, password_val, qualification_val)
    sql = "insert into doctor(first_name, last_name, email, password, qualifiaction) values (%s, %s, %s, %s, %s)"
    cursor.execute(sql, val)
    conn.commit()
    messagebox.showinfo("Success", "Registration successful!")

def create_main_page():
    main_page = tk.Frame(root)
    main_page.pack()

    label = tk.Label(main_page, text="Ehealthcare", font=("Helvetica", 20))
    label.pack(pady=10)

    button_view_profile = tk.Button(main_page, text="1. View Profile", command=create_view_profile_page)
    button_view_profile.pack(pady=10)

    button_registration = tk.Button(main_page, text="2. Registration", command=create_registration_page)
    button_registration.pack(pady=10)

def create_view_profile_page():
    view_profile_page = tk.Frame(root)
    view_profile_page.pack()

    label = tk.Label(view_profile_page, text="View Profile", font=("Helvetica", 16))
    label.pack(pady=10)

    global email_entry, password_entry, profile_text

    label_email = tk.Label(view_profile_page, text="Email:")
    label_email.pack(pady=5)
    email_entry = tk.Entry(view_profile_page)
    email_entry.pack(pady=5)

    label_password = tk.Label(view_profile_page, text="Password:")
    label_password.pack(pady=5)
    password_entry = tk.Entry(view_profile_page, show='*')
    password_entry.pack(pady=5)

    view_button = tk.Button(view_profile_page, text="View Profile", command=view_profile)
    view_button.pack(pady=10)

    profile_text = tk.Text(view_profile_page, height=10, width=30)
    profile_text.pack(pady=10)

    back_button = tk.Button(view_profile_page, text="Back", command=view_profile_page.destroy)
    back_button.pack(pady=10)

def create_registration_page():
    registration_page = tk.Frame(root)
    registration_page.pack()

    label = tk.Label(registration_page, text="Registration", font=("Helvetica", 16))
    label.pack(pady=10)

    global id_entry, first_name_entry, last_name_entry, email_entry_reg, password_entry_reg, qualification_entry

    # label_id = tk.Label(registration_page, text="ID:")
    # label_id.pack(pady=5)
    # id_entry = tk.Entry(registration_page)
    # id_entry.pack(pady=5)

    label_first_name = tk.Label(registration_page, text="First Name:")
    label_first_name.pack(pady=5)
    first_name_entry = tk.Entry(registration_page)
    first_name_entry.pack(pady=5)

    label_last_name = tk.Label(registration_page, text="Last Name:")
    label_last_name.pack(pady=5)
    last_name_entry = tk.Entry(registration_page)
    last_name_entry.pack(pady=5)

    label_email_reg = tk.Label(registration_page, text="Email:")
    label_email_reg.pack(pady=5)
    email_entry_reg = tk.Entry(registration_page)
    email_entry_reg.pack(pady=5)

    label_password_reg = tk.Label(registration_page, text="Password:")
    label_password_reg.pack(pady=5)
    password_entry_reg = tk.Entry(registration_page, show='*')
    password_entry_reg.pack(pady=5)

    label_qualification = tk.Label(registration_page, text="Qualification:")
    label_qualification.pack(pady=5)
    qualification_entry = tk.Entry(registration_page)
    qualification_entry.pack(pady=5)

    register_button = tk.Button(registration_page, text="Register", command=register)
    register_button.pack(pady=10)

    back_button = tk.Button(registration_page, text="Back", command=registration_page.destroy)
    back_button.pack(pady=10)

if __name__ == "__main__":
    conn = mysql.connector.connect(host='localhost', username='root', password='sadneya@sam05', database='Ehealthcare')
    cursor = conn.cursor()

    root = tk.Tk()
    root.title("Ehealthcare System")

    create_main_page()

    root.mainloop()

    conn.close()
