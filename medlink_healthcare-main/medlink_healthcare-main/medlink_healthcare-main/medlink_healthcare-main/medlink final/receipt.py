from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_receipt_pdf(patient_name,consultation_fee, lab_test_fee, medication_fee, patient_id, other_fees, doctor_name, appointment_details):
    # Constants
    gst_rate = 0.18
    extra_charges = 100

    # Calculate subtotal
    subtotal = consultation_fee + lab_test_fee + medication_fee

    # Calculate GST amount
    gst_amount = subtotal * gst_rate

    # Calculate total amount including GST and extra charges
    total_amount = subtotal + gst_amount + other_fees + extra_charges

    # Create PDF canvas
    pdf_filename = f"Receipt_Patient_{patient_id}.pdf"
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)

    # Define coordinates for content
    x_offset = 50
    y_offset = 750
    line_height = 20
    star=10
    # Set font and size
    pdf_canvas.setFont("Helvetica-Bold", 16)

    # Add header
    pdf_canvas.drawString(200, 800, "Healthcare Receipt")

    # Set font and size for body text
    pdf_canvas.setFont("Helvetica", 12)

    # Add patient details
    pdf_canvas.drawString(x_offset, y_offset, f"Patient ID: {patient_id}")
    y_offset -= line_height
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

    pdf_canvas.drawString(x_offset + 20, y_offset, f"Consultation Fee: ${consultation_fee:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Lab Test Fee: ${lab_test_fee:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Medication Fee: ${medication_fee:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"GST (18%): ${gst_amount:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Other Fees: ${other_fees:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset + 20, y_offset, f"Extra Charges: ${extra_charges:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star

    # Add total amount
    pdf_canvas.drawString(x_offset, y_offset, f"Total Amount: ${total_amount:.2f}")
    y_offset -= line_height
    pdf_canvas.drawString(x_offset, y_offset, "*"*50)
    y_offset -= star
    # Save the PDF file
    pdf_canvas.save()

# Example usage
patient_id = 1
doctor_name = "Dr. John Doe"
patient_name="abcd"
appointment_details = ["2024-03-21", "10:00 AM"]
consultation_fee = 200
lab_test_fee = 150
medication_fee = 100
other_fees = 50

generate_receipt_pdf(patient_name,consultation_fee, lab_test_fee, medication_fee, patient_id, other_fees, doctor_name, appointment_details)

