from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os

def generate_invoice_pdf(username, amount, invoice_id):
    path = f"invoices/invoice_{invoice_id}.pdf"
    os.makedirs("invoices", exist_ok=True)

    c = canvas.Canvas(path, pagesize=A4)
    c.drawString(100, 800, f"1DMASW Invoice #{invoice_id}")
    c.drawString(100, 770, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, 740, f"Billed To: {username}")
    c.drawString(100, 700, f"Service: Seismic Processing Credit")
    c.drawString(100, 670, f"Amount: ${amount:.2f} USD")
    c.drawString(100, 640, "Thank you for your business.")
    c.save()

    return path
