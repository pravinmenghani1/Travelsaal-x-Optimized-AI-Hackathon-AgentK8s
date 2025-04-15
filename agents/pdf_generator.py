# agents/pdf_generator.py

from fpdf import FPDF
import os
import re

def replace_emojis(text):
    """
    Replace specific unsupported emojis with text equivalents.
    """
    text = text.replace("🚨", "[Risk]")
    text = text.replace("✅", "[OK]")
    return text

class PDFReportGenerator(FPDF):
    def __init__(self, title="EKS Operational Report"):
        super().__init__()
        self.title = title
        
        # Get the absolute path to the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # Define font paths using absolute paths
        self.base_font_path = os.path.join(project_root, "fonts")
        self.regular_font_path = os.path.join(self.base_font_path, "DejaVuSans.ttf")
        self.bold_font_path = os.path.join(self.base_font_path, "DejaVuSans-Bold.ttf")
        self.italic_font_path = os.path.join(self.base_font_path, "DejaVuSans-Oblique.ttf")
        
        # Debug print to see the paths
        print(f"Font paths being used:")
        print(f"Regular: {self.regular_font_path}")
        print(f"Bold: {self.bold_font_path}")
        print(f"Italic: {self.italic_font_path}")
        
        # Verify fonts exist
        if not all(os.path.exists(p) for p in [self.regular_font_path, self.bold_font_path, self.italic_font_path]):
            print("Warning: Some font files are missing!")
            print(f"Contents of fonts directory: {os.listdir(self.base_font_path)}")
        
        # Register fonts with error handling
        try:
            self.add_font("DejaVu", "", self.regular_font_path, uni=True)
            self.add_font("DejaVu", "B", self.bold_font_path, uni=True)
            self.add_font("DejaVu", "I", self.italic_font_path, uni=True)
        except Exception as e:
            print(f"Error registering fonts: {e}")
            # Fallback to Arial
            self.set_font("Arial", size=12)
    
    def header(self):
        try:
            self.set_font("DejaVu", "B", 16)
        except:
            self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.title, border=False, ln=1, align="C")
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        try:
            self.set_font("DejaVu", "", 8)
        except:
            self.set_font("Arial", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(report_text: str, output_filename: str = "eks_operational_report.pdf"):
    try:
        report_text = replace_emojis(report_text)
        pdf = PDFReportGenerator()
        pdf.add_page()
        
        try:
            pdf.set_font("DejaVu", "", 12)
        except:
            pdf.set_font("Arial", "", 12)

        for line in report_text.splitlines():
            if line.strip():
                pdf.multi_cell(0, 10, line)
            else:
                pdf.ln(5)

        # Try to save in different locations
        try:
            pdf.output(output_filename)
        except:
            # If original location fails, try /tmp
            output_filename = f"/tmp/{output_filename}"
            pdf.output(output_filename)
            
        return output_filename
    
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        raise
