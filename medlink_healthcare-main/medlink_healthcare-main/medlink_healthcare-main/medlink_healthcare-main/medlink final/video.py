import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import pyautogui
import time
import pyperclip


def get_current_url():
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

    pyautogui.click(1166, 466)
    time.sleep(1)
    # Click on 'Enter a code or link'
    pyautogui.click(476, 781)
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

    current_url = pyperclip.paste()  # Get the contents of the clipboard
    
    return current_url
    
    
def make_video_call():
    # Ask for patient name
    patient_name = ask_for_name("Patient")
    if not patient_name:
        return

    # Ask for doctor name
    doctor_name = ask_for_name("Doctor")
    if not doctor_name:
        return

    # Get patient and doctor IDs from the database
    patient_id = fetch_id_from_name(patient_name, "patient_info")
    doctor_id = fetch_id_from_name(doctor_name, "doctor_info")

    if not patient_id:
        messagebox.showerror("Error", f"Patient with name '{patient_name}' not found.")
        return
    if not doctor_id:
        messagebox.showerror("Error", f"Doctor with name '{doctor_name}' not found.")
        return

    # Get the meeting URL
    meeting_url = get_current_url()

    # Generate an access code (you may use any suitable method)
    access_code = "123456"  # Example access code

    # Insert the video call details into the database
    insert_video_call(patient_id, doctor_id, meeting_url, access_code)

def ask_for_name(title):
    name = None
    name_window = tk.Toplevel(root)
    name_window.title(f"Enter {title}")

    def submit_name():
        nonlocal name
        name = name_entry.get()
        name_window.destroy()

    name_label = ttk.Label(name_window, text=f"Enter {title} name:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    name_entry = ttk.Entry(name_window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    submit_button = ttk.Button(name_window, text="Submit", command=submit_name)
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    name_window.wait_window(name_window)
    return name

def fetch_id_from_name(name, table):
    try:
        # Establish a MySQL database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ehealthcare"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Prepare the SQL query to fetch ID from name
        select_query = f"SELECT id FROM {table} WHERE Name = %s"

        # Execute the SQL query
        cursor.execute(select_query, (name,))

        # Fetch the result
        result = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        connection.close()

        if result:
            return result[0]
        else:
            return None

    except mysql.connector.Error as error:
        print("Error fetching ID from name:", error)
        return None



def insert_video_call(patient_id, doctor_id, meeting_url, access_code):
    try:
        # Establish a MySQL database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ehealthcare"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Prepare the SQL query to insert the video call details
        insert_query = """
        INSERT INTO video_calls (PatientID, DoctorID, MeetingID, AccessCode, CallDate, MeetingLink)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Get the current date and time
        call_date = datetime.now()

        # Execute the SQL query
        cursor.execute(insert_query, (patient_id, doctor_id, meeting_url, access_code, call_date, meeting_url))

        # Commit the transaction
        connection.commit()

        print("Video call details inserted successfully.")

    except mysql.connector.Error as error:
        print("Error inserting video call details:", error)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Call the function to make a video call
    make_video_call()

