# import pyautogui
# import time
# # # https://github.com/AdritoPramanik/Automation_Of_Google_Meet/tree/main

# # meetingID = pyautogui.prompt(text='Enter your meeting ID', title='Meeting ID', default='')
# # time.sleep(1)

# # # Open Microsoft Edge
# # pyautogui.press('win', interval=0.5)
# # time.sleep(1)
# # pyautogui.typewrite('microsoft edge', interval=0.5)
# # time.sleep(1)
# # pyautogui.press('enter', interval=0.5)
# # time.sleep(5)  # Adjust this delay based on your system's performance

# # # Type Google Meet URL
# # pyautogui.typewrite('https://meet.google.com/?authser=0', interval=0.3)
# # time.sleep(1)
# # pyautogui.press('enter', interval=0.5)
# # time.sleep(5)  # Adjust this delay based on your system's performance

# # # Click on Join Button
# # pyautogui.click(250, 570)
# # time.sleep(2)

# # # Type Meeting ID
# # pyautogui.typewrite(meetingID, interval=0.2)
# # time.sleep(1)

# # # Press Enter to Join
# # pyautogui.press('enter', interval=0.2)
# # time.sleep(9)

# # # Click on Camera and Microphone Buttons
# # pyautogui.click(400, 570)
# # time.sleep(2)
# # pyautogui.click(500, 570)
# # time.sleep(2)

# # # Alert and Confirmation
# # pyautogui.alert(text='We are entering a meeting', title='Info', button='OK')
# # time.sleep(1)

# # # Click on Join Meeting Button
# # pyautogui.click(990, 440)

# # print("Asked to join")

import pyautogui
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from login_and_signup import *
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'ehealthcare',
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
    BillID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT,
    AppointmentID INT,
    TotalAmount DECIMAL(10, 2),
    AdditionalDetails VARCHAR(255),
    BillDate DATE,
    FOREIGN KEY (PatientID) REFERENCES patient_info(id),
    FOREIGN KEY (AppointmentID) REFERENCES appointments(AppointmentID)
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
    global current_patient_id
    query = "SELECT * FROM patient_info WHERE Email= %s AND Password = %s"
    values = (p_mail, p_pass)
    user = fetch_data(query, values)

    if user:
        current_patient_id = user[0][0] 
        messagebox.showinfo("Login", "Patient login successful!")
        open_main_p()
        patient_id = get_logged_in_patient_id() 
    else:
        messagebox.showinfo("Login", "Invalid Contact number or password. Please try again!")

def get_logged_in_patient_id():
    global current_patient_id
    return current_patient_id

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
        messagebox.showinfo("Login", "Invalid Contact number or password. Please try again!")

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
            
def generate_meeting_id():
    # Simulate meeting ID generation logic (replace this with your actual logic)
    return "MEET123"

def generate_access_code():
    # Simulate access code generation logic (replace this with your actual logic)
    return "5678"

def fetch_patient_email(patient_name):
    # Replace this with your actual database query to fetch patient email
    # Assuming the query returns a single result, and the email is in the first column
    query = "SELECT Email FROM patient_info WHERE Name = %s"
    values = (patient_name,)
    result = fetch_data(query, values)
    if result:
        return result[0][0]
    else:
        return None

def send_email(recipient_email, meeting_link):
    # Replace these with your SMTP server details
    smtp_server = 'your_smtp_server.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'

    sender_email = 'your_email@gmail.com'
    subject = 'Meeting Link'
    body = f'Here is the link to join the meeting: {meeting_link}'

    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to SMTP server
    server.login(smtp_username, smtp_password)

    # Send email
    server.sendmail(sender_email, recipient_email, message.as_string())

    # Quit SMTP server
    server.quit()
    
def make_video_call():
    meeting_id = generate_meeting_id()

    # Open Microsoft Edge
    pyautogui.press('win', interval=0.5)
    time.sleep(1)
    pyautogui.typewrite('microsoft edge', interval=0.5)
    time.sleep(1)
    pyautogui.press('enter', interval=0.5)
    time.sleep(5)  # Adjust this delay based on your system's performance

    # Type Google Meet URL
    pyautogui.typewrite('https://meet.google.com/', interval=0.3)
    time.sleep(1)
    pyautogui.press('enter', interval=0.5)
    time.sleep(5)  # Adjust this delay based on your system's performance

    # Click on 'Join or start a meeting'
    pyautogui.click(175, 781)
    time.sleep(2)

    # Click on 'Create a new meeting'
    pyautogui.click(259, 782)
    time.sleep(2)

    # Copy the meeting code (adjust coordinates based on your screen)
    pyautogui.click(1156, 675)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    pyautogui.click(1166 ,466)
    time.sleep(1)
    # Click on 'Enter a code or link'
    pyautogui.click(476 ,781)
    time.sleep(1)

    # Paste the meeting code
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    # Press Enter to Join
    pyautogui.press('enter', interval=0.2)
    time.sleep(9)

    # Click on Camera and Microphone Buttons (Adjust coordinates based on your screen)
    pyautogui.click(817, 781)
    time.sleep(2)
    pyautogui.click(500, 570)
    time.sleep(2)

    # Alert and Confirmation
    pyautogui.alert(text='We are entering a meeting', title='Info', button='OK')
    time.sleep(1)

    # Click on Join Meeting Button (Adjust coordinates based on your screen)
    pyautogui.click(990, 440)
    patient_name=get_patient_name()
    patient_email = fetch_patient_email(patient_name)
    if not patient_email:
        print(f"Error: Email not found for the patient {patient_name}")
        return

    # Get the meeting link
    meeting_link = f'https://meet.google.com/{meeting_id}'

    # Send email to patient with the meeting link
    send_email(patient_email, meeting_link)

    print(f"Meeting link sent to patient {patient_name}")



# make_video_call()


# # # Display the mouse position
# import pyautogui

# # Display the mouse position
# print("Move your mouse over the desired location and press Ctrl+C to exit.")
# try:
#     while True:
#         x, y = pyautogui.position()
#         position_str = f'X: {x:4}, Y: {y:4}'
#         print(position_str, end='\r')
# except KeyboardInterrupt:
#     print('\nPosition capture ended.')
# x=259 y=782
# x=479 y=781
#  x=817 y=781