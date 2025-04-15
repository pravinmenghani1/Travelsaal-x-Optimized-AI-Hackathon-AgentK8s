# agents/pdf_generator.py

from fpdf import FPDF
import os
import re
from datetime import datetime

def replace_emojis(text):
    """
    Replace specific emojis and symbols with text equivalents.
    """
    emoji_map = {
        "🚨": "[RISK]",
        "✅": "[OK]",
        "💡": "[INFO]",
        "💸": "[COST]",
        "🔐": "[SECURITY]",
        "📈": "[MONITORING]",
        "⚙️": "[CI/CD]",
        "🧩": "[OTHER]",
        "🤖": "[AGENT]",
        # Add more emoji replacements as needed
    }
    
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    
    # Remove any remaining emojis or special characters that might cause issues
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

class PDFReportGenerator(FPDF):
    def __init__(self, title="EKS Operational Review Report"):
        super().__init__()
        self.title = title
        self.date = datetime.now().strftime("%Y-%m-%d")
    
    def header(self):
        # Header with Arial font
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, self.title, border=False, ln=1, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on {self.date}', border=False, ln=1, align='C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(report_text: str, output_filename: str = "eks_operational_report.pdf") -> str:
    """
    Generate a PDF report from the given text.
    
    Args:
        report_text (str): The report content to be converted to PDF
        output_filename (str): The name of the output PDF file
    
    Returns:
        str: The name of the generated PDF file
    """
    try:
        # Clean the text
        report_text = replace_emojis(report_text)

        # Create PDF object
        pdf = PDFReportGenerator()
        pdf.add_page()

        # Split the report into sections
        sections = report_text.split('\n\n')

        for section in sections:
            if not section.strip():
                continue

            # Check if this is a section header
            if any(keyword in section.lower() for keyword in 
                ['cluster health', 'cost optimization', 'security', 'monitoring', 'ci/cd', 'others']):
                pdf.chapter_title(section.strip())
            else:
                # Handle Risk and Recommendation subsections
                if 'Risk:' in section:
                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(0, 10, 'Risk:', ln=1)
                    pdf.chapter_body(section.replace('Risk:', '').strip())
                elif 'Recommendation:' in section:
                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(0, 10, 'Recommendation:', ln=1)
                    pdf.chapter_body(section.replace('Recommendation:', '').strip())
                else:
                    pdf.chapter_body(section)

        # Save the PDF
        try:
            pdf.output(output_filename)
            return output_filename
        except Exception as e:
            # If the default location fails, try to save in /tmp
            tmp_filename = f"/tmp/{output_filename}"
            pdf.output(tmp_filename)
            return tmp_filename

    except Exception as e:
        raise Exception(f"Failed to generate PDF: {str(e)}")

if __name__ == "__main__":
    # Test the PDF generation
    test_text = """
    Cluster Health
    Risk: Multiple nodes are experiencing issues
    Recommendation: Implement proper monitoring

    Cost Optimization
    Risk: Resources are underutilized
    Recommendation: Configure auto-scaling

    Security
    Risk: Weak security configurations
    Recommendation: Implement best practices
    """
    
    try:
        output_file = generate_pdf(test_text)
        print(f"PDF generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
