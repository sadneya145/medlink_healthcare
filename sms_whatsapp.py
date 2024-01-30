from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

# Corrected the method for initializing the Chrome driver
driver = webdriver.Chrome()

baseurl = "https://web.whatsapp.com"
driver.get(baseurl)

# Wait for the user to scan QR code manually
input("Scan the QR code and press Enter when ready...")

def send_whatsapp_message(phonenum, message):
    sameTab = baseurl + "/send?phone=" + str(phonenum)
    driver.get(sameTab)
    
    time.sleep(3)  # Adjust the sleep time according to your needs
    
    content = driver.switch_to.active_element
    content.send_keys(message)
    content.send_keys(Keys.RETURN)

    time.sleep(3)  # Adjust the sleep time according to your needs

# Sending appointment messages to patients
with open("patient_appointments.csv", newline='') as csvfile:
    readAppointments = csv.reader(csvfile)
    for phone, appointment_time in readAppointments:
        message = f"Dear patient, your appointment is scheduled for {appointment_time}. Please be on time."
        send_whatsapp_message(phone, message)

# Sending doctor's schedule messages
with open("doctor_schedule.csv", newline='') as csvfile:
    readSchedule = csv.reader(csvfile)
    for phone, schedule_info in readSchedule:
        message = f"Hello doctor, here is your schedule for the day: {schedule_info}."
        send_whatsapp_message(phone, message)

# Close the browser after sending messages
driver.quit()
