import tkinter as tk
import tkinter as ttk
from tkinter import messagebox
import re
import mysql.connector
from PIL import Image, ImageTk
from functools import partial
from make_appoinment import *
from tkcalendar import DateEntry
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from tkinter import scrolledtext
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tkinter import filedialog
import os
import shutil
import webbrowser
import ssl
import calendar
from datetime import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'Ehealthcare',
}

# Function to execute SQL queries
def execute_query(query, values=None):
    try:
        global conn
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
execute_query("""CREATE TABLE IF NOT EXISTS patient_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255),
    Name VARCHAR(255),
    Contact_no VARCHAR(255),
    Password VARCHAR(255),
    Age INT,  -- Change data type to INT for Age
    Gender VARCHAR(255),
    Diagnosis VARCHAR(255),
    INDEX (Name) )""")

# Create the doctor_info table
execute_query("""
CREATE TABLE IF NOT EXISTS doctor_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255),
    Name VARCHAR(255),
    Contact_no VARCHAR(255),
    Password VARCHAR(255),
    Qualifications VARCHAR(255),
    Speciality VARCHAR(255),
    Consultation_fee DECIMAL(10, 2),  -- Example column for consultation fee
    Lab_test_fee DECIMAL(10, 2),  -- Example column for lab test fee
    Medication_fee DECIMAL(10, 2),  -- Example column for medication fee
    Other_fees DECIMAL(10, 2),  -- Example column for additional fees
    INDEX (Name)
)

""")

# Create the appointments table with foreign key constraints
execute_query("""
CREATE TABLE IF NOT EXISTS appointments (
    AppointmentID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE,
    AppointmentDay VARCHAR(255),
    AppointmentTime TIME,  -- Ensure the column name is AppointmentTime
    AppointmentStatus VARCHAR(255),
    FOREIGN KEY (PatientID) REFERENCES patient_info(id),
    FOREIGN KEY (DoctorID) REFERENCES doctor_info(id)
)
""")

execute_query("""CREATE TABLE IF NOT EXISTS medical_records (
        RecordID INT AUTO_INCREMENT PRIMARY KEY,
        PatientID INT,
        DoctorID INT,
        FilePath VARCHAR(255),
        UploadDate DATE,
        FOREIGN KEY (PatientID) REFERENCES patient_info(id),
        FOREIGN KEY (DoctorID) REFERENCES doctor_info(id)
    )
    """)

execute_query("""
CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appointment_id INT,
    total_amount DECIMAL(10, 2),
    additional_details TEXT,
    FOREIGN KEY (patient_id) REFERENCES patient_info(id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(AppointmentID)
);
""")

# Create the video_calls table
execute_query("""
CREATE TABLE IF NOT EXISTS video_calls (
    CallID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    MeetingID VARCHAR(50),
    AccessCode VARCHAR(10),
    CallDate DATETIME,
    FOREIGN KEY (PatientID) REFERENCES patient_info(id),
    FOREIGN KEY (DoctorID) REFERENCES doctor_info(id)
)
""")

def get_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
current_patient_id =None
def p_signup(p_mail, p_pass, p_name, p_contact):
    query = "INSERT INTO patient_info (Email, Name, Contact_no, Password) VALUES (%s, %s, %s, %s)"
    values = (p_mail, p_name, p_contact, p_pass)
    execute_query(query, values)
    messagebox.showinfo("Signup", "Signed up successfully!")

def p_login(p_mail, p_pass):
    global current_patient_id  # Ensure you're modifying the global variable
    query = "SELECT id FROM patient_info WHERE Email= %s AND Password = %s"
    values = (p_mail, p_pass)
    user = fetch_data(query, values)

    if user:
        
        current_patient_id = user[0][0] 
        
        messagebox.showinfo("Login", "Patient login successful!")
        open_main_p(root)
        patient_id = get_logged_in_patient_id() 
    else:
        messagebox.showinfo("Login", "Invalid Email or password. Please try again!")
        open_signup_window("patient")

def get_logged_in_patient_id():
    global current_patient_id
    return current_patient_id

def d_signup(d_mail, d_pass, d_name, d_contact, d_qual, d_speciality):
    query = "INSERT INTO doctor_info (Email, Name, Contact_no, Password, Qualifications, Speciality) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (d_mail, d_name, d_contact, d_pass, d_qual, d_speciality)
    execute_query(query, values)
    messagebox.showinfo("Signup", "Signed up successfully!")

def d_login(d_mail, d_pass):
    global current_doctor_id
    query = "SELECT id FROM doctor_info WHERE Email = %s AND Password = %s"
    values = (d_mail, d_pass)
    user = fetch_data(query, values)

    if user:
        current_doctor_id = user[0][0]  # Assuming the first column is the doctor's ID
        messagebox.showinfo("Login", "Doctor login successful!")
        open_main_d()
        doctor_id = get_logged_in_doctor_id()  # Get the doctor ID immediately after login
        # Now you have the doctor_id available for further use
    else:
        messagebox.showinfo("Login", "Invalid email or password. Please try again!")
        open_signup_window("Doctor")    

def get_logged_in_doctor_id():
    global current_doctor_id
    return current_doctor_id

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

def open_doctor_window():
    root.withdraw()
    doctor_window = tk.Toplevel(root)
    doctor_window.geometry("1000x625")

    new_image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\doctor_l.png"
    new_pil_image = Image.open(new_image_path)
    new_tk_image = ImageTk.PhotoImage(new_pil_image)
    new_background_label = tk.Label(doctor_window, image=new_tk_image)
    new_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def doctor_login_clicked():
        doctor_window.destroy()
        open_login_window("Doctor")

    def doctor_signup_clicked():
        doctor_window.destroy()
        open_signup_window("Doctor")

    login_button = tk.Button(
        doctor_window,
        text="Login", font=("Helvetica", 14),
        command=doctor_login_clicked,
        bd=0,  # Border width
        highlightthickness=-1,  # Set to a negative value for transparency
        bg="#A9BABD",  # Background color (you can set this to an empty string or any transparent color)
    )
    login_button.place(relx=0.70, rely=0.4, anchor="center")

    signup_button = tk.Button(
        doctor_window,
        text="Signup", font=("Helvetica", 14),
        command=doctor_signup_clicked,
        bd=0,  # Border width
        highlightthickness=-1,  # Set to a negative value for transparency
        bg="#A9BABD", 
    )
    signup_button.place(relx=0.70, rely=0.6, anchor="center")

    button_width = int(doctor_window.winfo_screenwidth() / 70)
    button_height = int(doctor_window.winfo_screenheight() / 190)
    login_button.config(width=button_width, height=button_height)
    signup_button.config(width=button_width, height=button_height)

    doctor_window.mainloop()

def open_patient_window():
    root.withdraw()
    patient_window = tk.Toplevel(root)
    patient_window.geometry("1000x800")

    new_image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\eg.png"
    new_pil_image = Image.open(new_image_path).resize((1000, 800), Image.LANCZOS)
    new_tk_image = ImageTk.PhotoImage(new_pil_image)

    new_background_label = tk.Label(patient_window, image=new_tk_image)
    new_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def patient_login_clicked():
        patient_window.destroy()
        open_login_window("Patient")

    def patient_signup_clicked():
        patient_window.destroy()
        open_signup_window("Patient")

    login_button = tk.Button(
        patient_window,
        text="Login", font=("Helvetica", 14),
        command=patient_login_clicked,
        bd=0,  # Border width
        highlightthickness=-1,  # Set to a negative value for transparency
        bg="#A9BABD",  # Background color (you can set this to an empty string or any transparent color)
    )
    login_button.place(relx=0.70, rely=0.4, anchor="center")

    signup_button = tk.Button(
        patient_window,
        text="Signup", font=("Helvetica", 14),
        command=patient_signup_clicked,
        bd=0,  # Border width
        highlightthickness=-1,  # Set to a negative value for transparency
        bg="#A9BABD",  # Background color (you can set this to an empty string or any transparent color)
    )
    signup_button.place(relx=0.70, rely=0.6, anchor="center")

    button_width = int(patient_window.winfo_screenwidth() / 70)
    button_height = int(patient_window.winfo_screenheight() / 190)
    login_button.config(width=button_width, height=button_height)
    signup_button.config(width=button_width, height=button_height)

    patient_window.mainloop()

def open_login_window(user_type):
    root.withdraw()
    login_window = tk.Toplevel(root)
    login_window.title(f"{user_type} Login")
    login_window.geometry("1000x800")

    new_image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\login2.png"
    new_pil_image = Image.open(new_image_path).resize((1000, 800), Image.LANCZOS)
    new_tk_image = ImageTk.PhotoImage(new_pil_image)

    new_background_label = tk.Label(login_window, image=new_tk_image)
    new_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    email_label = tk.Label(login_window, text="Email:", width=25, height=3, bg="#A9BABD")
    email_label.place(relx=0.6, rely=0.4, anchor="center")

    email_entry = tk.Entry(login_window, width=25)
    email_entry.place(relx=0.9, rely=0.4, anchor="center")

    password_label = tk.Label(login_window, text="Password:", width=25, height=3, bg="#A9BABD")
    password_label.place(relx=0.6, rely=0.5, anchor="center")

    password_entry = tk.Entry(login_window, width=25, show='*')
    password_entry.place(relx=0.9, rely=0.5, anchor="center")

            
    def login():
        email = email_entry.get()
        password = password_entry.get()
        if validate_email(email) and password:
            if user_type == "Doctor":
                d_login(email, password)
                login_window.withdraw()
                open_main_d()
            else:
                p_login(email, password)
                login_window.withdraw()
                open_main_p(root)
        else:
            messagebox.showwarning("Login Error", "Please enter a valid email and password.")
            login_window.lift()

    login_button = tk.Button(login_window, text="Login", font=("Helvetica", 14), command=login, width=30, height=1,
                            bd=0, highlightthickness=0, bg="#A9BABD")
    login_button.place(relx=0.70, rely=0.8, anchor="center")

    not_user_button = tk.Button(login_window, text="Not a user? Signup here", font=("Helvetica", 14),
                                command=lambda: open_signup_window(user_type), width=30, height=1,
                                bd=0, highlightthickness=0, bg="#A9BABD")
    not_user_button.place(relx=0.70, rely=0.9, anchor="center")
    
    
    button_width = int(login_window.winfo_screenwidth() / 60)
    button_height = int(login_window.winfo_screenheight() / 270)
    login_button.config(width=button_width, height=button_height)
    not_user_button.config(width=button_width, height=button_height)

    login_window.mainloop()

def open_signup_window(user_type):
    root.withdraw()
    signup_window = tk.Toplevel(root)
    signup_window.title(f"{user_type} Signup")
    signup_window.geometry("1000x800")

    new_image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\login1.png"
    new_pil_image = Image.open(new_image_path).resize((1000, 800), Image.LANCZOS)
    new_tk_image = ImageTk.PhotoImage(new_pil_image)

    new_background_label = tk.Label(signup_window, image=new_tk_image)
    new_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    new_background_label = tk.Label(signup_window, image=new_tk_image)
    new_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    name_label = tk.Label(signup_window, text="Name:", width=25, height=3, bg="#A9BABD")
    name_label.place(relx=0.6, rely=0.1, anchor="center")

    name_entry = tk.Entry(signup_window)
    name_entry.place(relx=0.7, rely=0.1)

    email_label = tk.Label(signup_window, text="Email:", width=25, height=3, bg="#A9BABD")
    email_label.place(relx=0.6, rely=0.2, anchor="center")

    email_entry = tk.Entry(signup_window, width=30)
    email_entry.place(relx=0.7, rely=0.2)

    password_label = tk.Label(signup_window, text="Password:", width=25, height=3, bg="#A9BABD")
    password_label.place(relx=0.6, rely=0.3, anchor="center")

    password_entry = tk.Entry(signup_window, width=30, show='*')
    password_entry.place(relx=0.7, rely=0.3)

    contact_label = tk.Label(signup_window, text="Contact Number:", width=25, height=3, bg="#A9BABD")
    contact_label.place(relx=0.6, rely=0.4, anchor="center")

    contact_entry = tk.Entry(signup_window)
    contact_entry.place(relx=0.7, rely=0.4)

    if user_type == "Doctor":
        qual_label = tk.Label(signup_window, text="Qualifications:", width=25, height=3, bg="#A9BABD")
        qual_label.place(relx=0.6, rely=0.5, anchor="center")

        qual_entry = tk.Entry(signup_window)
        qual_entry.place(relx=0.7, rely=0.5)

        speciality_label = tk.Label(signup_window, text="Speciality:", width=25, height=3, bg="#A9BABD")
        speciality_label.place(relx=0.6, rely=0.6, anchor="center")

        speciality_entry = tk.Entry(signup_window)
        speciality_entry.place(relx=0.7, rely=0.6)

    def signup():
        email = email_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        contact = contact_entry.get()
        if validate_email(email) and password and name and contact and len(contact) == 10:
            if user_type == "Doctor":
                qual = qual_entry.get()
                speciality = speciality_entry.get()
                d_signup(email, password, name, contact, qual, speciality)
            else:
                p_signup(email, password, name, contact)
            messagebox.showinfo("Signup", "Signed up successfully!")
            signup_window.destroy()
            open_login_window(user_type)
        else:
            messagebox.showwarning("Signup Error", "Please fill in all fields with a valid email and a 10-digit contact number.")
            signup_window.lift()

    signup_button = tk.Button(signup_window, text="Signup", command=signup, font=("Helvetica", 14),  width=40, height=2,
                            bd=0, highlightthickness=0, bg="#A9BABD")
    signup_button.place(relx=0.70, rely=0.8, anchor="center")

    already_user_button = tk.Button(signup_window, text="Already a user? Login here", font=("Helvetica", 14),
                                    command=lambda: open_login_window(user_type), width=40, height=2,
                                    bd=0, highlightthickness=0, bg="#A9BABD")
    already_user_button.place(relx=0.70, rely=0.9, anchor="center")

    button_width = int(signup_window.winfo_screenwidth() / 60)
    button_height = int(signup_window.winfo_screenheight() / 270)
    signup_button.config(width=button_width, height=button_height)
    already_user_button.config(width=button_width, height=button_height)
    signup_window.mainloop()

def open_main_d():
    main_d = tk.Toplevel(root)
    main_d.geometry("1000x800")
    main_d.title("MedLink - Doctor Homepage")

    # Left Panel
    left_panel = tk.Frame(main_d, width=300, bg='lightgray', padx=10, pady=10)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    left_panel.pack_propagate(False)

    # MedLink Label
    tk.Label(left_panel, text="MedLink", font=('Helvetica', 18, 'bold'), bg='lightgray').pack(pady=30)

    # Doctor Buttons
    buttons = [
        ("My Profile", show_doctor_profile),
        ("View Appointments", open_doctor_profile),
        ("Enter Fees", open_fee_entry_frame),
        ("View Patient Records", fetch_patient_records)
    ]

    for text, command in buttons:
        button = tk.Button(left_panel, text=text, command=command, width=20, height=2)
        button.config(borderwidth=0, highlightthickness=0, bg="grey", fg="white", font=("Helvetica", 12))
        button.pack(pady=10)

    # Right Panel
    right_panel = tk.Frame(main_d, bg='white', padx=20, pady=20)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Load and display the image
    image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\Purple and Pink Flat Color UI Login Page Simple Desktop UI Prototype.png"
    img = Image.open(image_path)
    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(right_panel, image=photo)
    image_label.image = photo
    image_label.pack(side=tk.LEFT, padx=20)
   
    main_d.mainloop()
def fetch_patient_records():
    # Fetch the patient's medical records from the database
    records_query = """
    SELECT m.FilePath, m.UploadDate, p.Name AS FirstName, p.Contact_no AS Contact
    FROM medical_records m
    JOIN patient_info p ON m.PatientID = p.id
    """
    records = fetch_data(records_query)

    # Display the records in the GUI (Text widget) with open buttons
    if records:
        # Create a new window to display patient records
        records_window = tk.Toplevel(root)
        records_window.title("Patient Medical Records")
        records_window.geometry("500x300")

        for record in records:
            # Create a frame for each record
            record_frame = tk.Frame(records_window)
            record_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display patient name and contact on the left
            patient_info_label = tk.Label(record_frame, text=f"Patient: {record[2]}, Contact: {record[3]}")
            patient_info_label.pack(side=tk.LEFT)

            # Display file name and upload date in the middle
            file_info_label = tk.Label(record_frame, text=f"File: {os.path.basename(record[0])}, Upload Date: {record[1]}")
            file_info_label.pack(side=tk.LEFT)

            # Create an "Open" button on the right
            open_button = tk.Button(record_frame, text="Open", command=lambda f=record[0]: open_file(f))
            open_button.pack(side=tk.RIGHT)

    else:
        messagebox.showinfo("Patient Records", "No patient records found.")

def open_file_in_browser(file_path):
    if os.path.exists(file_path):
        # Use 'file://' to specify that it's a local file
        url = f'file://{file_path}'

        # Open the file in the default web browser
        webbrowser.open(url)
    else:
        print(f"File not found: {file_path}")

def open_fee_entry_frame():
    global fee_entry_frame
    fee_entry_frame = tk.Toplevel(root)
    fee_entry_frame.geometry("400x300")
    fee_entry_frame.title("Enter Fees")

    # Consultation Fee Entry
    consultation_fee_label = tk.Label(fee_entry_frame, text="Consultation Fee:")
    consultation_fee_label.pack(pady=5)

    consultation_fee_entry = tk.Entry(fee_entry_frame)
    consultation_fee_entry.pack(pady=5)

    # Lab Test Fee Entry
    lab_test_fee_label = tk.Label(fee_entry_frame, text="Lab Test Fee:")
    lab_test_fee_label.pack(pady=5)

    lab_test_fee_entry = tk.Entry(fee_entry_frame)
    lab_test_fee_entry.pack(pady=5)

    # Medication Fee Entry
    medication_fee_label = tk.Label(fee_entry_frame, text="Medication Fee:")
    medication_fee_label.pack(pady=5)

    medication_fee_entry = tk.Entry(fee_entry_frame)
    medication_fee_entry.pack(pady=5)

    # Other Fees Entry
    other_fees_label = tk.Label(fee_entry_frame, text="Other Fees:")
    other_fees_label.pack(pady=5)

    other_fees_entry = tk.Entry(fee_entry_frame)
    other_fees_entry.pack(pady=5)

    # Save Fees Button
    save_fees_button = tk.Button(fee_entry_frame, text="Save Fees", command=lambda: save_fees(
        consultation_fee_entry.get(),
        lab_test_fee_entry.get(),
        medication_fee_entry.get(),
        other_fees_entry.get()
    ))
    save_fees_button.pack(pady=10)

def save_fees(consultation_fee, lab_test_fee, medication_fee, other_fees):
    # Save the entered fees to the database or perform any necessary actions
    # You can use the fetch_data and execute_query functions for database operations
    # Example: Save the fees to the doctor_info table for the logged-in doctor
    doctor_id = get_logged_in_doctor_id()  # Implement a function to get the logged-in doctor's ID
    update_fees_query = """
    UPDATE doctor_info
    SET Consultation_fee = %s, Lab_test_fee = %s, Medication_fee = %s, Other_fees = %s
    WHERE id = %s
    """
    execute_query(update_fees_query, (consultation_fee, lab_test_fee, medication_fee, other_fees, doctor_id))
    messagebox.showinfo("Fees Updated", "Fees have been updated successfully!")

    # Close the fee entry frame after saving
    fee_entry_frame.destroy()

def generate_receipt_pdf(consultation_fee, lab_test_fee, medication_fee, other_fees, doctor_name, appointment_details, total_amount, patient_name):
    medical_records_directory = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medical_records"
    
    # Create the directory if it doesn't exist
    os.makedirs(medical_records_directory, exist_ok=True)

    # Create a PDF file
    pdf_filename = os.path.join(medical_records_directory, f"Receipt_Patient_{patient_name}.pdf")
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)
    gst_rate = 18
    extra_charges = 100

    # Calculate subtotal
    subtotal = consultation_fee + lab_test_fee + medication_fee

    # Calculate GST amount
    gst_amount = subtotal * gst_rate/100

    # Calculate total amount including GST and extra charges
    total_amount = subtotal + gst_amount + other_fees + extra_charges

    # Define coordinates for content
    x_offset = 50
    y_offset = 750
    line_height = 20
    star = 10

    # Set font and size
    pdf_canvas.setFont("Helvetica-Bold", 16)

    # Add header
    pdf_canvas.drawString(200, 800, "Healthcare Receipt")

    # Set font and size for body text
    pdf_canvas.setFont("Helvetica", 12)

    # Add patient details
    pdf_canvas.drawString(x_offset, y_offset, f"Patient Name: {patient_name}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star

    # Add doctor's name
    pdf_canvas.drawString(x_offset, y_offset, f"Doctor Name: {doctor_name}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star

    # Add appointment details
    pdf_canvas.drawString(x_offset, y_offset, "Appointment Details:")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Date: {appointment_details[0]}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Time: {appointment_details[1]}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star

    # Add charges breakdown
    pdf_canvas.drawString(x_offset, y_offset, "Charges Breakdown:")
    y_offset -= line_height

    pdf_canvas.drawString(x_offset + 20, y_offset, f"Consultation Fee: Rs.{consultation_fee:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Lab Test Fee: Rs.{lab_test_fee:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Medication Fee: Rs.{medication_fee:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"GST (18%): Rs.{gst_amount:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Other Fees: Rs.{other_fees:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Extra Charges: Rs.{extra_charges:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star

    # Add total amount
    pdf_canvas.drawString(x_offset, y_offset, f"Total Amount: Rs.{total_amount:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star

    # Save the PDF file
    pdf_canvas.save()
    
# Global variable to store doctor_name
doctor_name = None

def get_doctor_name():
    # Create a new window for entering doctor name
    name_window = tk.Toplevel(root)
    name_window.title("Enter Doctor Name")

    # Function to handle the submission of doctor name
    def submit_name():
        global doctor_name
        doctor_name = name_entry.get()
        name_window.destroy()  # Close the window after submitting the name

    # Entry widget for the doctor name
    name_label = ttk.Label(name_window, text="Enter Doctor's Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    name_entry = ttk.Entry(name_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    submit_button = ttk.Button(name_window, text="Submit", command=submit_name)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    name_window.wait_window(name_window)  # Wait for the window to be closed
    return doctor_name

def get_patient_name():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Execute the query to retrieve the patient's name
        cursor.execute("SELECT Name FROM patient_info WHERE id = %s", (current_patient_id,))
        patient_name = cursor.fetchone()
        
        if patient_name:
            return patient_name[0]  # Extracting the name from the tuple
        else:
            return None  # Patient not found
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def get_doctor_and_patient_names():
    doctor_name = ask_for_name("Doctor's Name")
    patient_name = ask_for_name("Patient's Name")
    return doctor_name, patient_name

def ask_for_name(title):
    name = None
    name_window = tk.Toplevel(root)
    name_window.title(title)

    def submit_name():
        nonlocal name
        name = name_entry.get()
        name_window.destroy()

    name_label = ttk.Label(name_window, text=f"Enter {title}:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    name_entry = ttk.Entry(name_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    submit_button = ttk.Button(name_window, text="Submit", command=submit_name)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    name_window.wait_window(name_window)
    return name

def generate_healthcare_receipt(appointment_id):
    doctor_name, patient_name = get_doctor_and_patient_names()

    if doctor_name and patient_name:
        # Fetch fees from the database or use default values
        doctor_id = get_logged_in_doctor_id()
        fees_query = "SELECT Consultation_fee, Lab_test_fee, Medication_fee, Other_fees FROM doctor_info WHERE id = %s"
        fees = fetch_data(fees_query, (doctor_id,))
        consultation_fee, lab_test_fee, medication_fee, other_fees = fees[0] if fees else (0, 0, 0, 0)

        # Fetch appointment date and time from the database
        appointment_details_query = """
        SELECT AppointmentDate, AppointmentTime
        FROM appointments
        WHERE AppointmentID = %s
        """
        appointment_details = fetch_data(appointment_details_query, (appointment_id,))
        appointment_date, appointment_time = appointment_details[0] if appointment_details else (None, None)

        # Calculate total amount
        total_amount = consultation_fee + lab_test_fee + medication_fee + other_fees

        # Save bill details to the database
        save_bill_to_database(patient_name, appointment_id, total_amount, "Additional Details")

        # Continue with generating the receipt PDF
        generate_receipt_pdf(consultation_fee, lab_test_fee, medication_fee, other_fees, doctor_name,
                            (appointment_date, appointment_time), total_amount, patient_name)
    else:
        messagebox.showerror("Name Error", "Please enter both doctor's and patient's names.")

def save_bill_to_database(patient_name, appointment_id, total_amount, additional_details):
    try:
        # Establish a MySQL database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ehealthcare"
        )

        with connection.cursor() as cursor:
            # Check if the patient name exists in patient_info table
            cursor.execute("SELECT id FROM patient_info WHERE Name = %s", (patient_name,))
            result = cursor.fetchone()
            if result:
                patient_id = result[0]
                # Patient name exists, proceed with the insertion
                insert_bill_query = """
                INSERT INTO bills (patient_id, appointment_id, total_amount, additional_details)
                VALUES (%s, %s, %s, %s)
                """
                # Execute the query with the provided parameters
                cursor.execute(insert_bill_query, (patient_id, appointment_id, total_amount, additional_details))

                # Commit the changes to the database
                connection.commit()
            else:
                messagebox.showerror("Patient Name Error", "Patient name does not exist.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to save bill to database: {err}")
    finally:
        # Close the database connection
        if connection and connection.is_connected():
            connection.close()
  
def show_doctor_profile():
    profile_page = tk.Toplevel(root)
    profile_page.geometry("400x300")
    profile_page.title("Doctor Profile")

    # Email Entry
    email_label = tk.Label(profile_page, text="Email:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(profile_page)
    email_entry.pack(pady=5)

    # Password Entry
    password_label = tk.Label(profile_page, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(profile_page, show='*')
    password_entry.pack(pady=5)

    # View Profile Button
    view_button = tk.Button(profile_page, text="View Profile", command=lambda: view_profile(email_entry, password_entry))
    view_button.pack(pady=10)

    # Text widget to display the doctor's profile
    profile_text = tk.Text(profile_page, height=10, width=30)
    profile_text.pack(pady=10)

    def view_profile(email_entry, password_entry):
        email = email_entry.get()
        password = password_entry.get()
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM doctor_info WHERE email=%s AND password=%s", (email, password))
            result = cursor.fetchone()

            if result:
                profile_text.delete(1.0, tk.END)
                profile_text.insert(tk.END,
                                    f"Email: {result[1]}\nName: {result[2]}\nContact Number: {result[3]}\nQualification: {result[5]}\nSpeciality: {result[6]}")
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

def open_doctor_profile():
    profile_page = tk.Toplevel(root)
    profile_page.geometry("400x300")
    profile_page.title("Doctor Profile")

    # Email Entry
    email_label = tk.Label(profile_page, text="Email:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(profile_page)
    email_entry.pack(pady=5)

    # Password Entry
    password_label = tk.Label(profile_page, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(profile_page, show='*')
    password_entry.pack(pady=5)

    # Show Appointments Button
    show_appointments_button = tk.Button(profile_page, text="Show Appointments", command=lambda: show_doctor_appointments(email_entry.get(), password_entry.get()))
    show_appointments_button.pack(pady=10)

def show_doctor_appointments(email, password):
    # Validate email and password
    if not validate_email(email) or not password:
        messagebox.showwarning("Validation Error", "Please enter a valid email and password.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch doctor ID based on email
        cursor.execute("SELECT id FROM doctor_info WHERE Email = %s AND Password = %s", (email, password))
        doctor_id = cursor.fetchone()

        if doctor_id:
            doctor_id = doctor_id[0]

            # Fetch appointments data for the given doctor ID
            cursor.execute("""
                SELECT * FROM appointments
                INNER JOIN patient_info ON appointments.PatientID = patient_info.id
                WHERE appointments.DoctorID = %s
                ORDER BY appointments.AppointmentDate, appointments.AppointmentTime
            """, (doctor_id,))

            appointments_data = cursor.fetchall()

            if appointments_data:
                # Create a new window to display the appointments
                appointments_window = tk.Toplevel(root)
                appointments_window.title("Doctor Appointments")
                appointments_window.geometry("500x400")

                # Create a text widget to display the appointments
                appointments_text = tk.Text(appointments_window, height=20, width=50)
                appointments_text.pack(pady=10)

                # Display appointments in chronological order
                for appointment in appointments_data:
                    appointments_text.insert(tk.END,
                                              f"AppointmentID: {appointment[0]}\n"
                                              f"PatientName: {appointment[4]}\n"
                                              f"AppointmentDate: {appointment[3]}\n"
                                              f"AppointmentTime: {appointment[5]}\n"
                                              f"AppointmentStatus: {appointment[6]}\n\n")
            else:
                messagebox.showinfo("Appointments", "No appointments found for the given email and password.")
        else:
            messagebox.showerror("Error", "Doctor not found. Please check the email and password.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    view_patient_button = tk.Button(appointments_window, text=f"View {appointment[4]}'s Profile", command=lambda app_id=appointment[0], pat_id=appointment[1]: view_patient_profile_and_bill(app_id, pat_id))
    view_patient_button.pack(pady=5)

def view_patient_profile_and_bill(appointment_id, patient_id):
    # Fetch patient information based on patient_id
    patient_info_query = "SELECT * FROM patient_info WHERE id = %s"
    patient_info = fetch_data(patient_info_query, (patient_id,))

    if not patient_info:
        messagebox.showinfo("Patient Info", "Patient information not found.")
        return

    # Display patient information
    patient_profile_window = tk.Toplevel(root)
    patient_profile_window.title(f"Patient Profile - {patient_info[0][2]}")
    patient_profile_window.geometry("400x300")

    tk.Label(patient_profile_window, text="Patient Information", font=('Helvetica', 14, 'bold')).pack(pady=10)

    for field, value in zip(["ID", "Email", "Name", "Contact Number", "Password", "Age", "Diagnosis"], patient_info[0]):
        tk.Label(patient_profile_window, text=f"{field}: {value}").pack()

    # Button to give a bill
    give_bill_button = tk.Button(patient_profile_window, text="Give Bill", command=lambda app_id=appointment_id, pat_id=patient_id: generate_healthcare_receipt(app_id))
    give_bill_button.pack(pady=10)
    
def get_patient_name():
    # Create a new window for entering patient name
    name_window = tk.Toplevel(root)
    name_window.title("Enter Patient Name")

    # Function to handle the submission of patient name
    def submit_name():
        global current_patient_name
        current_patient_name = name_entry.get()
        create_appointment_frame(name_window,current_patient_name)
        

    # Entry widget for the patient name
    name_label = ttk.Label(name_window, text="Enter Your Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    name_entry = ttk.Entry(name_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    submit_button = ttk.Button(name_window, text="Submit", command=submit_name)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

def open_main_p(root):
    if hasattr(open_main_p, 'info_displayed') and open_main_p.info_displayed:
        # If info has already been displayed, return without creating a new window
        return
    main_p = tk.Toplevel(root)
    main_p.geometry("1000x800")
    main_p.title("MedLink - Doctor Homepage")
    main_p.protocol("WM_DELETE_WINDOW", root.quit)

    # Left Panel
    left_panel = tk.Frame(main_p, width=300, bg='lightgray', padx=10, pady=10)
    left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    left_panel.pack_propagate(False)

    # MedLink Label
    tk.Label(left_panel, text="MedLink", font=('Helvetica', 18, 'bold'), bg='lightgray').pack(pady=30)

    # Buttons
    buttons = [
        ("My Profile", show_patient_profile),
        ("Make Appointments", get_patient_name),
        ("Show Appointments", open_patient_profile),
        ("Chat with AI bot", launch_chatbot),
        ("Bill Payments", show_pdf_files),
        ("Medical Records", upload_medical_records),
        ("Show Records", show_uploaded_records)
    ]

    for text, command in buttons:
        button = tk.Button(left_panel, text=text, command=command, width=20, height=2)
        button.config(borderwidth=0, highlightthickness=0, bg="grey", fg="white", font=("Helvetica", 12))
        button.pack(pady=10)

    # Right Panel
    right_panel = tk.Frame(main_p, bg='white', padx=20, pady=20)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Load and display the image
    image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\patient_home.png"
    img = Image.open(image_path)

    # Display the image using Tkinter
    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(right_panel, image=photo)
    image_label.image = photo  # Keep a reference to the image to prevent garbage collection
    image_label.pack(side=tk.LEFT, padx=20)

def show_pdf_files():
    # Specify the directory where medical records (PDF files) are stored

    medical_records_directory = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medical_records"


    # Get a list of PDF files in the directory
    pdf_files = [file for file in os.listdir(medical_records_directory) if file.endswith(".pdf")]

    if pdf_files:
        # Create a new window to display PDF files
        pdf_window = tk.Toplevel(root)
        pdf_window.title("PDF Files")
        pdf_window.geometry("500x300")

        # Create a frame for displaying PDF files
        pdf_frame = tk.Frame(pdf_window)
        pdf_frame.pack(fill=tk.X, padx=10, pady=5)

        for pdf_file in pdf_files:
            # Create a frame for each PDF file
            pdf_file_frame = tk.Frame(pdf_frame)
            pdf_file_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display file name on the left
            file_name_label = tk.Label(pdf_file_frame, text=pdf_file)
            file_name_label.pack(side=tk.LEFT)

            # Create an "Open" button on the right
            open_button = tk.Button(pdf_file_frame, text="Open", command=lambda f=pdf_file: open_pdf(os.path.join(medical_records_directory, f)))
            open_button.pack(side=tk.RIGHT)

    else:
        tk.messagebox.showinfo("No PDF Files", "No PDF files found in the specified directory.")

def open_pdf(file_path):
    try:
        os.system(file_path)
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to open PDF file: {str(e)}")

def upload_medical_records():
    files = filedialog.askopenfilenames(title="Select Medical Records", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if files:
        # Save file paths to the database
        save_records_to_database(files, current_patient_id)

        # Move files to a specific directory (optional)
        move_files_to_directory(files)

        messagebox.showinfo("Upload Successful", "Medical records uploaded successfully!")

def save_records_to_database(file_paths, patient_id):
    # Implement your database logic to save file paths
    # For example, you could have a table with columns: PatientID, FilePath, UploadDate, etc.
    # Insert records into this table with patient_id and file_paths

    # Sample code (replace with your actual database logic)
    for file_path in file_paths:
        # Insert into the records table with patient_id and file_path
        insert_query = "INSERT INTO medical_records (PatientID, FilePath) VALUES (%s, %s)"
        execute_query(insert_query, (patient_id, file_path))

def move_files_to_directory(files):
    # Move uploaded files to a specific directory (optional)
    destination_directory = "medical_records"
    os.makedirs(destination_directory, exist_ok=True)

    for file_path in files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_directory, file_name)

        # Copy the file to the destination directory
        shutil.copy(file_path, destination_path)

def show_uploaded_records():
    # Fetch the patient's medical records from the database
    records_query = "SELECT FilePath, UploadDate FROM medical_records WHERE PatientID = %s"
    records = fetch_data(records_query, (current_patient_id,))

    # Display the records in the GUI (Text widget) with open buttons
    if records:
        # Create a new window to display patient records
        records_window = tk.Toplevel(root)
        records_window.title("Uploaded Medical Records")
        records_window.geometry("500x300")

        for record in records:
            # Create a frame for each record
            record_frame = tk.Frame(records_window)
            record_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display file name on the left
            file_name_label = tk.Label(record_frame, text=os.path.basename(record[0]))
            file_name_label.pack(side=tk.LEFT)

            # Create an "Open" button on the right
            open_button = tk.Button(record_frame, text="Open", command=lambda f=record[0]: open_file(f))
            open_button.pack(side=tk.RIGHT)

    else:
        messagebox.showinfo("Patient Records", "No medical records found.")

def open_file(file_path):
    # Open the file using the default system application
    webbrowser.open(file_path)

def appointment_details(appointment_id):
    # Fetch appointment details for the given appointment ID
    appointment_query = """
    SELECT appointments.AppointmentDate, appointments.AppointmentTime, doctor_info.Name
    FROM appointments
    INNER JOIN doctor_info ON appointments.DoctorID = doctor_info.id
    WHERE appointments.AppointmentID = %s
    """
    return fetch_data(appointment_query, (appointment_id,))

def create_appointment_frame(root, patient_name):
    def submit_appointment():
        selected_doctor = doctor_combobox.get()
        appointment_date = cal.get_date().strftime("%m/%d/%Y")  # Convert datetime.date to string
        appointment_day = cal.get_date().strftime("%A")  # Get day from the selected date
        appointment_time = time_entry.get()
        appointment_status = status_combobox.get()
    
        # Check if appointment date is in the past
        if cal.get_date() < datetime.now().date():
            messagebox.showerror("Error", "Appointment date cannot be in the past.")
            return

        # Check if appointment time is valid
        try:
            appointment_time_obj = datetime.strptime(appointment_time, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM format.")
            return

        # Check if appointment time is in the past
        current_time = datetime.now().time()
        if cal.get_date() == datetime.now().date() and appointment_time_obj < current_time:
            messagebox.showerror("Error", "Appointment time cannot be in the past.")
            return

        schedule_appointment(patient_name, selected_doctor, appointment_date, appointment_day, appointment_time, appointment_status)

        # Fetch email from the result (assuming the first tuple and first element)
        receiver_email = fetch_data("SELECT Email FROM patient_info WHERE Name = %s", (patient_name,))
        if receiver_email:
            receiver_email = receiver_email[0][0]
        else:
            messagebox.showerror("Error", "Email not found for the given patient name.")
            return

        print(f"Receiver Email: {receiver_email}")
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'sadneyasam05@gmail.com'
        password = 'ehpy ztem lfvl bdec'

        # Create a MIME object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Appointment Schedule'

        # Create the body of the email with clickable links
        body = f"Appointment made for {patient_name} with {selected_doctor} on {appointment_day}, {appointment_date} at {appointment_time}.\nStatus: {appointment_status}\n\n"
        body += "Click the following links for more details:\n"
        body += f"- [Doctor's Profile](http://link_to_doctor_profile)\n"
        body += f"- [Hospital Information](http://link_to_hospital_info)\n"
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=ssl.create_default_context())  # Use SSL context
                server.login(sender_email, password)

                # Send the email
                server.sendmail(sender_email, receiver_email, message.as_string())

            messagebox.showinfo("Success", 'Mail sent successfully!')

        except smtplib.SMTPException as e:
            messagebox.showerror("Error", f'Error sending email: {e}')

    def schedule_appointment(patient_name, doctor_name, appointment_date, appointment_day, appointment_time, appointment_status):
        # Convert appointment date to MySQL-compatible format (YYYY-MM-DD)
        appointment_date_mysql = datetime.strptime(appointment_date, "%m/%d/%Y").strftime("%Y-%m-%d")

        # Fetch patient and doctor IDs based on names
        patient_id = fetch_data("SELECT id FROM patient_info WHERE Name = %s", (patient_name,))
        doctor_id = fetch_data("SELECT id FROM doctor_info WHERE Name = %s", (doctor_name,))

        # Check if patient and doctor IDs are retrieved
        if patient_id and doctor_id:
            # Unpack the fetched IDs from the result tuples
            patient_id = patient_id[0][0]
            doctor_id = doctor_id[0][0]

            # Insert the appointment into the appointments table
            query = """
            INSERT INTO appointments (PatientID, DoctorID, AppointmentDate, AppointmentDay, AppointmentTime, AppointmentStatus)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (patient_id, doctor_id, appointment_date_mysql, appointment_day, appointment_time, appointment_status)
            execute_query(query, values)
            messagebox.showinfo("Appointment", "Appointment scheduled successfully!")
        else:
            messagebox.showerror("Error", "Patient or doctor not found. Please check the names and try again.")
        

    # Create and configure the frame
    frame = ttk.Frame(root, padding="50")  # Adjust the padding value to make the frame bigger
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    # Create labels and entry widgets
    name_label = ttk.Label(frame, text="Patient Name:")
    name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
    name_label.configure(background="#A9BABD", foreground="white", font=("Helvetica", 12))

    name_entry = ttk.Entry(frame, width=30, state="readonly")
    name_entry.insert(0, patient_name)
    name_entry.grid(row=0, column=1, sticky=tk.W, pady=10)  # Increased pady value for spacing

    # Sample list of doctors, replace it with your own list
    doctors = fetch_data("SELECT Name FROM doctor_info")
    doctors = [doctor[0] for doctor in doctors]
    doctor_label = ttk.Label(frame, text="Select Doctor:")
    doctor_label.grid(row=1, column=0, sticky=tk.W, pady=5)
    doctor_label.configure(background="#A9BABD", foreground="white", font=("Helvetica", 12))

    doctor_combobox = ttk.Combobox(frame, values=doctors, state="readonly")
    doctor_combobox.grid(row=1, column=1, sticky=tk.W, pady=10)  # Increased pady value for spacing

    date_label = ttk.Label(frame, text="Appointment Date:")
    date_label.grid(row=2, column=0, sticky=tk.W, pady=5)
    date_label.configure(background="#A9BABD", foreground="white", font=("Helvetica", 12))

    cal = DateEntry(frame, width=30, background='darkblue', foreground='white', borderwidth=2)
    cal.grid(row=2, column=1, sticky=tk.W, pady=10)  # Increased pady value for spacing

    # Sample list of appointment statuses, replace it with your own list
    statuses = ["Confirm", "Cancel"]
    status_label = ttk.Label(frame, text="Appointment Status:")
    status_label.grid(row=3, column=0, sticky=tk.W, pady=5)
    status_label.configure(background="#A9BABD", foreground="white", font=("Helvetica", 12))

    status_combobox = ttk.Combobox(frame, values=statuses, state="readonly")
    status_combobox.grid(row=3, column=1, sticky=tk.W, pady=10)  # Increased pady value for spacing

    time_label = ttk.Label(frame, text="Appointment Time:")
    time_label.grid(row=4, column=0, sticky=tk.W, pady=5)
    time_label.configure(background="#A9BABD", foreground="white", font=("Helvetica", 12))

    time_entry = ttk.Entry(frame, width=30)
    time_entry.grid(row=4, column=1, sticky=tk.W, pady=10)  # Increased pady value for spacing

    # Create a button to submit the appointment
    submit_button = ttk.Button(frame, text="Submit Appointment", command=submit_appointment)
    submit_button.grid(row=5, column=0, columnspan=2, pady=20)  # Adjust the pady value to provide more space

    # Create a label to display the result
    result_label = ttk.Label(frame, text="")
    result_label.grid(row=6, column=0, columnspan=2, pady=20)  # Adjust the pady value to provide more space

    return frame


def open_patient_profile():
    profile_page = tk.Toplevel(root)
    profile_page.geometry("400x300")
    profile_page.title("Patient Profile")

    # Email Entry
    email_label = tk.Label(profile_page, text="Email:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(profile_page)
    email_entry.pack(pady=5)

    # Password Entry
    password_label = tk.Label(profile_page, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(profile_page, show='*')
    password_entry.pack(pady=5)

    # Show Appointments Button
    show_appointments_button = tk.Button(profile_page, text="Show Appointments", command=lambda: show_patient_appointments(email_entry.get(), password_entry.get()))
    show_appointments_button.pack(pady=10)

def show_patient_appointments(email, password):
    # Validate email and password
    if not validate_email(email) or not password:
        messagebox.showwarning("Validation Error", "Please enter a valid email and password.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch patient ID based on email
        cursor.execute("SELECT id FROM patient_info WHERE Email = %s AND Password = %s", (email, password))
        patient_id = cursor.fetchone()

        if patient_id:
            patient_id = patient_id[0]

            # Fetch appointments data for the given patient ID
            cursor.execute("""
                SELECT * FROM appointments
                INNER JOIN doctor_info ON appointments.DoctorID = doctor_info.id
                WHERE appointments.PatientID = %s
                ORDER BY appointments.AppointmentDate, appointments.AppointmentTime
            """, (patient_id,))

            appointments_data = cursor.fetchall()

            if appointments_data:
                # Create a new window to display the appointments
                appointments_window = tk.Toplevel(root)
                appointments_window.title("Patient Appointments")
                appointments_window.geometry("500x400")

                # Create a text widget to display the appointments
                appointments_text = tk.Text(appointments_window, height=20, width=50)
                appointments_text.pack(pady=10)

                # Display appointments in chronological order
                for appointment in appointments_data:
                    appointments_text.insert(tk.END,
                                              f"AppointmentID: {appointment[0]}\n"
                                              f"DoctorName: {appointment[2]}\n"
                                              f"AppointmentDate: {appointment[3]}\n"
                                              f"AppointmentTime: {appointment[5]}\n"
                                              f"AppointmentStatus: {appointment[6]}\n\n")
            else:
                messagebox.showinfo("Appointments", "No appointments found for the given email and password.")
        else:
            messagebox.showerror("Error", "Patient not found. Please check the email and password.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def launch_chatbot():
    def chat_about_disease(query):
    # Add your logic to handle different types of diseases and their information
    # For simplicity, categorize based on common disease types
        if 'flu' in query:
            return "The flu, or influenza, is a contagious respiratory illness caused by influenza viruses. Symptoms include fever, cough, sore throat, body aches, and fatigue."

        elif 'diabetes' in query:
            return "Diabetes is a chronic condition that affects how your body turns food into energy. There are different types of diabetes, including type 1 and type 2. Management involves medication, diet, and lifestyle changes."

        elif 'hypertension' in query or 'high blood pressure' in query:
            return "Hypertension, or high blood pressure, is a condition where the force of the blood against the artery walls is consistently too high. It can lead to serious health issues, so it's important to manage it through lifestyle changes and medication."

        elif 'asthma' in query:
            return "Asthma is a chronic respiratory condition that causes difficulty in breathing. It is often triggered by factors like allergies or environmental factors. Treatment involves medications and lifestyle management."

        elif 'arthritis' in query:
            return "Arthritis is a condition that causes inflammation in the joints, leading to pain and stiffness. There are different types of arthritis, and treatment options include medications, physical therapy, and lifestyle changes."

        elif 'migraine' in query:
            return "A migraine is a type of headache characterized by severe pain, nausea, and sensitivity to light and sound. Migraines can be triggered by various factors, and treatment may include medications and lifestyle adjustments."

        elif 'osteoporosis' in query:
            return "Osteoporosis is a condition characterized by weakened bones, making them more prone to fractures. It is more common in older adults, especially women. Treatment involves medications, a healthy diet, and weight-bearing exercises."

        elif 'pneumonia' in query:
            return "Pneumonia is an infection that inflames the air sacs in one or both lungs. Symptoms include cough, fever, and difficulty breathing. Treatment typically involves antibiotics and supportive care."

        elif 'anemia' in query:
            return "Anemia is a condition where there is a deficiency of red blood cells or hemoglobin in the blood, leading to fatigue and weakness. Treatment depends on the underlying cause and may include iron supplements or other medications."

        elif 'cancer' in query:
            return "Cancer is a group of diseases characterized by the uncontrolled growth and spread of abnormal cells. Treatment options vary depending on the type and stage of cancer and may include surgery, chemotherapy, and radiation therapy."

        elif 'alzheimer' in query or 'dementia' in query:
            return "Alzheimer's disease is a progressive neurodegenerative disorder that affects memory and cognitive function. There is no cure, but treatment may involve medications and supportive care."

        elif 'heart disease' in query:
            return "Heart disease refers to a variety of conditions that affect the heart, including coronary artery disease and heart failure. Management involves lifestyle changes, medications, and, in some cases, surgery."

        elif 'stroke' in query:
            return "A stroke occurs when there is a disruption of blood flow to the brain, leading to damage. Symptoms include sudden numbness, confusion, and difficulty speaking. Treatment depends on the type of stroke but may involve medication or surgery."

        elif 'chronic kidney disease' in query:
            return "Chronic kidney disease is a condition where the kidneys gradually lose their function over time. Treatment involves managing underlying conditions, medications, and sometimes dialysis or kidney transplant."

        elif 'liver cirrhosis' in query:
            return "Liver cirrhosis is a late stage of scarring of the liver caused by many forms of liver diseases and conditions. It can lead to liver failure. Management includes lifestyle changes and treatment of underlying causes."

        elif 'parkinson' in query:
            return "Parkinson's disease is a progressive nervous system disorder that affects movement. Symptoms include tremors, stiffness, and difficulty with balance. Treatment involves medications and, in some cases, surgery."

        elif 'thyroid' in query:
            return "Thyroid disorders, such as hypothyroidism or hyperthyroidism, affect the thyroid gland's function. Treatment may involve medication to regulate thyroid hormones."

        elif 'ulcerative colitis' in query:
            return "Ulcerative colitis is a chronic inflammatory bowel disease that causes inflammation and ulcers in the colon. Treatment involves medications and, in severe cases, surgery."

        elif 'osteoarthritis' in query:
            return "Osteoarthritis is a degenerative joint disease that occurs when the protective cartilage that cushions the ends of bones wears down over time. Treatment includes pain management and lifestyle modifications."

        elif 'fibromyalgia' in query:
            return "Fibromyalgia is a disorder characterized by widespread musculoskeletal pain, fatigue, and sleep disturbances. Treatment involves pain management, exercise, and stress reduction."

        else:
            return "I'm sorry, I don't have information on that specific disease. It's recommended to consult with a healthcare professional for accurate advice."

    # def say(text):
        # engine = pyttsx3.init()
        # engine.say(text)
        # engine.runAndWait()

    def provide_remedies():
        remedies = "Here are some general suggestions:\n" \
                   "1. Maintain a healthy diet and stay hydrated.\n" \
                   "2. Get regular exercise to promote overall well-being.\n" \
                   "3. Ensure proper sleep for better health.\n" \
                   "4. Manage stress through relaxation techniques.\n" \
                   "5. Consult with a healthcare professional for personalized advice."
        chat_history.insert(tk.END, f"Chatbot: {remedies}\n\n")

    def help_user():
        help_text = "How may I help you today? You can ask about specific diseases or request general health information."
        chat_history.insert(tk.END, f"Chatbot: {help_text}\n\n")

    def send_message():
        user_message = user_entry.get()

        if 'remedies' in user_message:
            provide_remedies()
        elif 'help' in user_message:
            help_user()
        else:
            response = chat_about_disease(user_message)
            chat_history.insert(tk.END, f"User: {user_message}\n")
            chat_history.insert(tk.END, f"Chatbot: {response}\n\n")

    root = tk.Tk()
    root.geometry("400x400")
    root.title("Patient Chatbot")

    # User Entry
    user_entry = tk.Entry(root, width=30)
    user_entry.pack(pady=10)

    # Send Button
    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack(pady=10)

    # Chat History
    chat_history = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
    chat_history.pack(pady=10)

    # Provide initial help message
    help_user()

    root.mainloop()

def show_patient_profile():
    profile_page = tk.Toplevel(root)
    profile_page.geometry("400x300")
    profile_page.title("Patient Profile")

    # Email Entry
    email_label = tk.Label(profile_page, text="Email:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(profile_page)
    email_entry.pack(pady=5)

    # Password Entry
    password_label = tk.Label(profile_page, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(profile_page, show='*')
    password_entry.pack(pady=5)

    # View Profile Button
    view_button = tk.Button(profile_page, text="View Profile", command=lambda: view_patient_profile(email_entry,password_entry))
    view_button.pack(pady=10)

    # Text widget to display the patient's profile
    profile_text = tk.Text(profile_page, height=10, width=30)
    profile_text.pack(pady=10)

    def view_patient_profile(email_entry,password_entry):
        email = email_entry.get()
        password = password_entry.get()
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM patient_info WHERE email=%s AND password=%s", (email, password))
            result = cursor.fetchone()

            if result:
                profile_text.delete(1.0, tk.END)
                profile_text.insert(tk.END,
                                    f"Email: {result[1]}\nName: {result[2]}\nContact No: {result[3]}\nGender: {result[6]}\nAge: {result[5]}\nDiagnosis: {result[7]}")
            else:
                messagebox.showerror("Error", "Patient not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
   
def validate_email(email):
    if re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        return True
    return False

root = tk.Tk()
root.title("eHealthcare")
w = 1000
h = 800
root.geometry(f"{w}x{h}")

image_path = r"medlink_healthcare-main\medlink_healthcare-main\medlink_healthcare-main\medlink final\main.png"
pil_image = Image.open(image_path).resize((1000, 800), Image.LANCZOS)
tk_image = ImageTk.PhotoImage(pil_image)

background_label = tk.Label(root, image=tk_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

doctor_button = tk.Button(root, text="Doctor", font=("Helvetica", 14), command=open_doctor_window, width=35, height=2,
                          bd=0, highlightthickness=0, bg="#A9BABD")
doctor_button.place(relx=0.70, rely=0.4, anchor="center")

patient_button = tk.Button(root, text="Patient", font=("Helvetica", 14), command=open_patient_window, width=35, height=2,
                           bd=0, highlightthickness=0, bg="#A9BABD")
patient_button.place(relx=0.70, rely=0.5, anchor="center")

button_width = int(w / 120)
button_height = int(h / 120)
root.mainloop()
