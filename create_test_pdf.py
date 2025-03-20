from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_test_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Add text
    c.setFont("Helvetica", 16)
    c.drawString(1*inch, 10*inch, "Test Document")
    
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, 9*inch, "This is a sample PDF document created for testing the PDF analyzer.")
    c.drawString(1*inch, 8.5*inch, "It contains both text and simple graphics to test different aspects")
    c.drawString(1*inch, 8*inch, "of the document processing capabilities.")
    
    # Add some simple graphics
    c.setStrokeColor(colors.blue)
    c.rect(1*inch, 4*inch, 2*inch, 2*inch, fill=1)
    
    c.setStrokeColor(colors.red)
    c.circle(5*inch, 5*inch, 1*inch, fill=1)
    
    c.showPage()
    c.save()

if __name__ == "__main__":
    create_test_pdf("test.pdf")
