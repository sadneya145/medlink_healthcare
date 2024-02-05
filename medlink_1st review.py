import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# MySQL connection parameters
db_config = {
    'host': 'Premnaths-MacBook-Air.local',
    'user': 'root',
    'password': '#1Anshianay',
    'database': 'db',
}

# Function to execute SQL queries
def execute_query(query, values=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Create the patient_info table
execute_query("""
CREATE TABLE IF NOT EXISTS patient_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Name VARCHAR(255),
    Contact_no VARCHAR(255),
    Password VARCHAR(255),
    Age VARCHAR(255), 
    Gender VARCHAR(255), 
    Diagnosis VARCHAR(255)
)
""")

# Create the doctor_info table
execute_query("""
CREATE TABLE IF NOT EXISTS doctor_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Name VARCHAR(255),
    Contact_no VARCHAR(255),
    Password VARCHAR(255),
    Qualifications VARCHAR(255),
    Speciality VARCHAR(255)
)
""")

def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def p_signup(p_mail, p_pass, p_name, p_contact):
    query = "INSERT INTO patient_info (Email, Name, Contact_no, Password) VALUES (%s, %s, %s, %s)"
    values = (p_mail, p_name, p_contact, p_pass)
    execute_query(query, values)
    messagebox.showinfo("Signup", "Signed up successfully!")

def p_login(p_mail, p_pass):
    query = "SELECT * FROM patient_info WHERE Email = %s AND Password = %s"
    values = (p_mail, p_pass)
    user = fetch_data(query, values)

    if user:
        messagebox.showinfo("Login", "Patient login successful!")
        create_patient_homepage()
    else:
        messagebox.showinfo("Login", "Invalid email or password. Please try again!")

def d_signup(d_mail, d_pass, d_name, d_contact, d_qual, d_speciality):
    query = "INSERT INTO doctor_info (Email, Name, Contact_no, Password, Qualifications, Speciality) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (d_mail, d_name, d_contact, d_pass, d_qual, d_speciality)
    execute_query(query, values)
    messagebox.showinfo("Signup", "Signed up successfully!")

def d_login(d_mail, d_pass):
    query = "SELECT * FROM doctor_info WHERE Email = %s AND Password = %s"
    values = (d_mail, d_pass)
    user = fetch_data(query, values)

    if user:
        messagebox.showinfo("Login", "Doctor login successful!")
        create_doctor_homepage()
    else:
        messagebox.showinfo("Login", "Invalid email or password. Please try again!")

def fetch_data(query, values=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def patient_my_profile():
    global name_entry, age_entry, gender_var, diagnosis_entry 
    def save_patient_info():
        # Function to save patient information
        patient_name = name_entry.get()
        patient_age = age_entry.get()
        patient_gender = gender_var.get()
        patient_diagnosis = diagnosis_entry.get("1.0", tk.END)

        save_patient_to_db(patient_name, patient_age, patient_gender, patient_diagnosis)

    def save_patient_to_db(name, age, gender, diagnosis):
        query = "INSERT INTO patient_info (Name, Age, Gender, Diagnosis) VALUES (%s, %s, %s, %s)"
        values = (name, age, gender, diagnosis)
        execute_query(query, values)

    def clear_fields():
        # Function to clear input fields
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        gender_var.set("Male")  # Set default gender to Male
        diagnosis_entry.delete("1.0", tk.END)

    # Create a new window
    profile_window = tk.Toplevel()
    profile_window.title("Patient Information Profile")
    profile_window.geometry(f"{w}x{h}")

    # MedLink
    tk.Label(profile_window, text="MedLink", font=('Helvetica', 23)).pack(pady=10)

    # Patient Information Title
    tk.Label(profile_window, text="Patient Information Profile", font=('Helvetica', 18)).pack(pady=10)

    # Create and place widgets
    frame = ttk.Frame(profile_window)
    frame.pack()

    # Patient Name
    ttk.Label(frame, text="Name:").pack(pady=5)
    name_entry = ttk.Entry(frame, width=30)
    name_entry.pack(pady=1)

    # Patient Age
    ttk.Label(frame, text="Age:").pack(pady=5)
    age_entry = ttk.Entry(frame, width=10)
    age_entry.pack(pady=1)

    # Patient Gender
    ttk.Label(frame, text="Gender:").pack(pady=5)
    gender_var = tk.StringVar()
    gender_combobox = ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female", "Other"])
    gender_combobox.pack(pady=1)
    gender_combobox.set("Male")

    # Patient Diagnosis
    ttk.Label(frame, text="Diagnosis:").pack(pady=5)
    diagnosis_entry = tk.Text(frame, width=30, height=5)
    diagnosis_entry.pack(pady=1)

    # Save Button
    save_button = ttk.Button(frame, text="Save", command=save_patient_info)
    save_button.pack(pady=5, padx=10)

    # Clear Button
    clear_button = ttk.Button(frame, text="Clear", command=clear_fields)
    clear_button.pack(pady=5, padx=10)

# Global variable for company information
company_info_text = """
Welcome to MedLink,
Your Trusted Healthcare Partner!

MedLink is committed to providing exceptional healthcare 
services. Our platform connects doctors and patients 
seamlessly, ensuring quality care and a smooth experience.

Explore the features designed to make your healthcare 
journey efficient and comfortable. For any assistance, 
feel free to reach out to our support team.

- The MedLink Team
"""

def create_doctor_homepage():
    homepage = tk.Toplevel(root)
    homepage.title("MedLink - Doctor Homepage")
    homepage.geometry(f"{w}x{h}")

    # Left Panel
    left_panel = tk.Frame(homepage, width=300, bg='lightgray', padx=10, pady=10)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    left_panel.pack_propagate(False)

    # MedLink Label
    tk.Label(left_panel, text="MedLink", font=('Helvetica', 18, 'bold'), bg='lightgray').pack(pady=30)

    # Doctor Buttons
    tk.Button(left_panel, text="My Profile", command=show_doctor_profile,width=20, height=2).pack(pady=20)
    tk.Button(left_panel, text="View Appointments", command=show_appointments,width=20, height=2).pack(pady=20)

    # Right Panel
    right_panel = tk.Frame(homepage, bg='white', padx=20, pady=20)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # MedLink Company Information
    tk.Label(right_panel, text=company_info_text, font=('Helvetica', 12)).pack(pady=10)
    
def create_patient_homepage():
    homepage = tk.Toplevel(root)
    homepage.title("MedLink - Patient Homepage")
    homepage.geometry(f"{w}x{h}")

    # Left Panel
    left_panel = tk.Frame(homepage, width=300,bg='lightgray', padx=10, pady=10)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    left_panel.pack_propagate(False)

    # MedLink Label
    tk.Label(left_panel, text="MedLink", font=('Helvetica', 18, 'bold'), bg='lightgray').pack(pady=30)

    # Patient Buttons
    tk.Button(left_panel, text="My Profile", command=patient_my_profile,width=20, height=2).pack(pady=15)
    tk.Button(left_panel, text="View Appointments", command=show_appointments,width=20, height=2).pack(pady=15)
    tk.Button(left_panel, text="Search Doctors", command=search_doctors,width=20, height=2).pack(pady=15)
    tk.Button(left_panel, text="Talk to AI Chatbot", command=talk_to_chatbot,width=20, height=2).pack(pady=15)

    # Right Panel
    right_panel = tk.Frame(homepage, bg='white', padx=20, pady=20)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # MedLink Company Information
    tk.Label(right_panel, text=company_info_text, font=('Helvetica', 12)).pack(pady=10)

def show_doctor_profile():
    messagebox.showinfo("Doctor Profile", "This is the doctor's profile.")

def show_appointments():
    messagebox.showinfo("Appointments", "Viewing Appointments.")

def search_doctors():
    messagebox.showinfo("Search Doctors", "Searching for doctors.")

def talk_to_chatbot():
    messagebox.showinfo("AI Chatbot", "Talking to AI Chatbot.")
    
def create_signup_window(user_type):
    # Close the main window
    root.iconify()

    signup_window = tk.Toplevel(root)
    signup_window.title(f"MedLink - {user_type} Signup")
    signup_window.geometry(f"800x500")  # Adjust the size as needed

    # Entry widgets dictionary
    entry_widgets = {}

    # Labels
    tk.Label(signup_window, text="MedLink", font=('Helvetica', 23)).pack(pady=10)
    tk.Label(signup_window, text=f'{user_type} Signup', font=('Helvetica', 18)).pack(pady=10)

    # Create and place entry widgets
    labels = ["Name", "Email", "Password", "Contact Number"]
    if user_type == "Doctor":
        labels.extend(["Qualification", "Speciality"])

    for label in labels:
        frame = tk.Frame(signup_window)
        frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(frame, text=f"{label}: ", font=('Helvetica', 13)).pack(side=tk.LEFT, padx=(250, 10))
        entry = tk.Entry(frame, width=25)
        entry.pack(side=tk.LEFT, padx=(15, 10))
        entry_widgets[label] = entry

    # Signup button function
    def signup():
        # Accessing entry widgets
        name_entry = entry_widgets["Name"].get()
        email_entry = entry_widgets["Email"].get()
        password_entry = entry_widgets["Password"].get()
        contact_entry = entry_widgets["Contact Number"].get()

        if user_type == "Doctor":
            qualification_entry = entry_widgets["Qualification"].get()
            speciality_entry = entry_widgets["Speciality"].get()

            # Call doctor signup function
            d_signup(email_entry, password_entry, name_entry, contact_entry, qualification_entry, speciality_entry)
        elif user_type == "Patient":
            # Call patient signup function
            p_signup(email_entry, password_entry, name_entry, contact_entry)
        login()

    # Already a user? Login button function
    def login():
        signup_window.destroy()  # Close the signup window

        # Open login window
        login_window = tk.Toplevel(root)
        login_window.title(f"MedLink - {user_type} Login")
        login_window.geometry(f"{w}x{h}")

        # Labels
        tk.Label(login_window, text="MedLink", font=('Helvetica', 23)).pack(pady=10)
        tk.Label(login_window, text=f'{user_type} Login', font=('Helvetica', 18)).pack(pady=10)

        # Entry fields
        tk.Label(login_window, text="Email: ").pack(pady=10)
        email_entry = tk.Entry(login_window, width=30)
        email_entry.pack(pady=5)

        tk.Label(login_window, text="Password: ").pack(pady=5)
        password_entry = tk.Entry(login_window, width=30, show='*')
        password_entry.pack(pady=5)

        # Login button function
        def user_login():
            if user_type == "Doctor":
                # Call doctor login function
                d_login(email_entry.get(), password_entry.get())
            elif user_type == "Patient":
                # Call patient login function
                p_login(email_entry.get(), password_entry.get())

        # Login button
        btn_login = tk.Button(login_window, text='Login', command=user_login, width=23, height=3)
        btn_login.pack(pady=20)

    # Signup button
    btn_signup = tk.Button(signup_window, text='Signup', command=signup, width=23, height=3)
    btn_signup.pack(pady=20)

    # Already a user? Login button
    btn_login = tk.Button(signup_window, text=f'Already a user? Login', command=login)
    btn_login.pack()


# Main window
root = tk.Tk()
root.title("MedLink")

# Set the window dimensions
w = 800
h = 500
root.geometry(f"{w}x{h}")


# Labels
tk.Label(root, text="MedLink", font=('Helvetica', 23)).pack(pady=20)
tk.Label(root, text='Welcome to "MedLink"!', font=('Helvetica', 18)).pack()

# Buttons
btn_doctor = tk.Button(root, text='Doctor Signup', command=lambda: create_signup_window("Doctor"), width=23, height=3)
btn_doctor.pack(pady=20)

btn_patient = tk.Button(root, text='Patient Signup', command=lambda: create_signup_window("Patient"), width=23, height=3)
btn_patient.pack()


root.mainloop()