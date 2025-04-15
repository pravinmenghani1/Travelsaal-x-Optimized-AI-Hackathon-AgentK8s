# agents/pdf_generator.py

from fpdf import FPDF
import os
import re

def replace_emojis(text):
    """
    Replace specific unsupported emojis with text equivalents.
    """
    emoji_map = {
        "🚨": "[Risk]",
        "✅": "[OK]",
        "💡": "[Cluster Health]",
        "💸": "[Cost Optimization]",
        "🔐": "[Security]",
        "📈": "[Monitoring]",
        "⚙️": "[CI/CD]",
        "🧩": "[Others]",
        "🤖": "[Agent]"
    }
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    return text

class PDFReportGenerator(FPDF):
    def __init__(self, title="EKS Operational Report"):
        super().__init__()
        self.title = title
        
        # Get font paths using os.path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_dir = os.path.join(os.path.dirname(current_dir), 'fonts')
        
        # Define font paths
        regular_font = os.path.join(font_dir, "DejaVuSans.ttf")
        bold_font = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
        italic_font = os.path.join(font_dir, "DejaVuSans-Oblique.ttf")
        
        print(f"Font directory: {font_dir}")
        print(f"Regular font path: {regular_font}")
        
        # Register fonts with error handling
        try:
            if os.path.exists(regular_font):
                self.add_font("DejaVu", "", regular_font, uni=True)
            if os.path.exists(bold_font):
                self.add_font("DejaVu", "B", bold_font, uni=True)
            if os.path.exists(italic_font):
                self.add_font("DejaVu", "I", italic_font, uni=True)
            self.set_font("DejaVu", "", 12)
            print("Custom fonts loaded successfully")
        except Exception as e:
            print(f"Error loading custom fonts: {str(e)}")
            self.set_font("Arial", size=12)
            print("Using Arial font as fallback")
    
    def header(self):
        try:
            self.set_font("DejaVu", "B", 16)
        except:
            self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        try:
            self.set_font("DejaVu", "", 8)
        except:
            self.set_font("Arial", "", 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(report_text: str, output_filename: str = "eks_operational_report.pdf"):
    """
    Generate a PDF report from the given text.
    """
    try:
        # Clean the text
        report_text = replace_emojis(report_text)
        
        # Create PDF object
        pdf = PDFReportGenerator()
        pdf.add_page()
        
        # Set font with fallback
        try:
            pdf.set_font("DejaVu", "", 12)
        except:
            pdf.set_font("Arial", "", 12)

        # Write content
        for line in report_text.splitlines():
            if line.strip():
                pdf.multi_cell(0, 10, line)
            else:
                pdf.ln(5)

        # Try to save the PDF
        try:
            # Try to save in /tmp first
            tmp_filename = os.path.join('/tmp', os.path.basename(output_filename))
            pdf.output(tmp_filename)
            return tmp_filename
        except Exception as e:
            print(f"Error saving to /tmp: {str(e)}")
            # If /tmp fails, try current directory
            pdf.output(output_filename)
            return output_filename
            
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        raise

if __name__ == "__main__":
    # Test the PDF generation
    test_text = """
    EKS Operational Review
    
    Cluster Health
    Risk: Multiple nodes are experiencing issues
    Recommendation: Implement proper monitoring
    """
    
    try:
        output_file = generate_pdf(test_text)
        print(f"Test PDF generated successfully: {output_file}")
    except Exception as e:
        print(f"Test PDF generation failed: {str(e)}")
