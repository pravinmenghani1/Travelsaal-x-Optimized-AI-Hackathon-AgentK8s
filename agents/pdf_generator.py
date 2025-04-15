# agents/pdf_generator.py

from fpdf import FPDF
import os
import re
from pathlib import Path

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
        
        # Get the repository root path using Path for better cross-platform compatibility
        repo_root = Path(__file__).parent.parent.absolute()
        font_dir = repo_root / "fonts"
        
        # Print debug information
        print(f"Repository root: {repo_root}")
        print(f"Font directory: {font_dir}")
        print(f"Font directory exists: {font_dir.exists()}")
        if font_dir.exists():
            print(f"Font directory contents: {list(font_dir.glob('*.ttf'))}")
        
        # Define font paths
        self.fonts = {
            'regular': str(font_dir / "DejaVuSans.ttf"),
            'bold': str(font_dir / "DejaVuSans-Bold.ttf"),
            'italic': str(font_dir / "DejaVuSans-Oblique.ttf")
        }
        
        # Register fonts with error handling
        try:
            for style, path in self.fonts.items():
                if Path(path).exists():
                    print(f"Loading font: {path}")
                    if style == 'regular':
                        self.add_font("DejaVu", "", path, uni=True)
                    elif style == 'bold':
                        self.add_font("DejaVu", "B", path, uni=True)
                    elif style == 'italic':
                        self.add_font("DejaVu", "I", path, uni=True)
                else:
                    print(f"Font file not found: {path}")
            
            # Test if fonts were loaded
            self.set_font("DejaVu", "", 12)
            print("Fonts loaded successfully")
            
        except Exception as e:
            print(f"Error loading fonts: {str(e)}")
            print("Falling back to Arial font")
            self.set_font("Arial", size=12)
    
    def header(self):
        try:
            self.set_font("DejaVu", "B", 16)
        except Exception as e:
            print(f"Header font error: {str(e)}")
            self.set_font("Arial", "B", 16)
            
        self.cell(0, 10, self.title, border=False, ln=1, align="C")
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        try:
            self.set_font("DejaVu", "", 8)
        except Exception as e:
            print(f"Footer font error: {str(e)}")
            self.set_font("Arial", "", 8)
            
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(report_text: str, output_filename: str = "eks_operational_report.pdf"):
    """
    Generate a PDF report from the given text.
    Args:
        report_text (str): The text content to be converted to PDF
        output_filename (str): The desired name of the output PDF file
    Returns:
        str: The path to the generated PDF file
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
        except Exception as e:
            print(f"Font setting error: {str(e)}")
            pdf.set_font("Arial", "", 12)

        # Write content
        for line in report_text.splitlines():
            if line.strip():
                pdf.multi_cell(0, 10, line)
            else:
                pdf.ln(5)

        # Try to save the PDF
        try:
            print(f"Attempting to save PDF to: {output_filename}")
            pdf.output(output_filename)
            print(f"PDF saved successfully to: {output_filename}")
        except Exception as e:
            print(f"Error saving to primary location: {str(e)}")
            # Try alternate location
            tmp_filename = f"/tmp/{Path(output_filename).name}"
            print(f"Attempting to save PDF to alternate location: {tmp_filename}")
            pdf.output(tmp_filename)
            output_filename = tmp_filename
            print(f"PDF saved successfully to alternate location: {output_filename}")
            
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
    
    Cost Optimization
    Risk: Resources are underutilized
    Recommendation: Configure auto-scaling
    """
    
    try:
        output_file = generate_pdf(test_text)
        print(f"Test PDF generated successfully: {output_file}")
    except Exception as e:
        print(f"Test PDF generation failed: {str(e)}")
