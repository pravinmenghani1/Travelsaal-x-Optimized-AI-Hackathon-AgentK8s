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

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.title = "EKS Operational Report"
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(report_text: str, output_filename: str = "eks_operational_report.pdf"):
    """
    Generate a PDF report from the given text.
    """
    try:
        # Clean the text
        report_text = replace_emojis(report_text)
        
        # Create PDF object
        pdf = PDFReport()
        pdf.add_page()
        
        # Process and write content
        sections = report_text.split('\n')
        for line in sections:
            line = line.strip()
            if not line:
                pdf.ln(5)
                continue
                
            # Handle different types of content
            if any(marker in line for marker in ["Risk:", "Recommendation:"]):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 10, line, 0, 1)
            else:
                pdf.set_font('Arial', '', 11)
                pdf.multi_cell(0, 10, line)

        # Save the PDF
        try:
            # Try to save in /tmp first
            tmp_filename = os.path.join('/tmp', 'eks_report.pdf')
            pdf.output(tmp_filename)
            return tmp_filename
        except Exception as e:
            print(f"Failed to save in /tmp: {e}")
            # If /tmp fails, try current directory
            current_dir_file = 'eks_report.pdf'
            pdf.output(current_dir_file)
            return current_dir_file
            
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
