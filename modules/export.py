import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from typing import Tuple

class ExcelDataPDF(FPDF):
    def __init__(self, title_text: str):
        super().__init__()
        self.title_text = title_text

    def header(self):
        # Logo placeholder or corporate banner
        self.set_fill_color(30, 41, 59)  # Deep Slate Navy
        self.rect(0, 0, 210, 30, 'F')
        
        # Title text
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, self.title_text, ln=True, align='C')
        
        # Subtitle
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, f"Diekspor pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True, align='C')
        self.ln(12)

    def footer(self):
        # Page numbers
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Halaman {self.page_no()}/{{nb}}", align='C')

def export_to_csv(df: pd.DataFrame, filename: str) -> str:
    """Export DataFrame to CSV in the assets/exports directory."""
    os.makedirs("assets/exports", exist_ok=True)
    file_path = os.path.join("assets/exports", filename)
    df.to_csv(file_path, index=False, encoding='utf-8')
    return file_path

def export_to_excel(df: pd.DataFrame, filename: str) -> str:
    """Export DataFrame to Excel in the assets/exports directory."""
    os.makedirs("assets/exports", exist_ok=True)
    file_path = os.path.join("assets/exports", filename)
    df.to_excel(file_path, index=False, engine='openpyxl')
    return file_path

def export_to_pdf(df: pd.DataFrame, filename: str) -> str:
    """Export DataFrame (up to 500 rows for performance and readability) to PDF."""
    os.makedirs("assets/exports", exist_ok=True)
    file_path = os.path.join("assets/exports", filename)

    pdf = ExcelDataPDF("Laporan Data Excel - Excel Data Center")
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Helvetica", size=9)

    # Determine columns to export (limit to top 6 columns to fit nicely in A4 portrait)
    cols = [col for col in df.columns if col != "Foto"][:6]
    
    # Calculate cell widths based on number of columns to fit inside margins (190mm total width)
    col_width = 190 / len(cols)

    # Draw Table Header
    pdf.set_fill_color(71, 85, 105)  # lighter slate gray
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    for col in cols:
        pdf.cell(col_width, 8, str(col), border=1, align="C", fill=True)
    pdf.ln()

    # Draw Table Rows (limit to first 500 rows to avoid extremely large pdfs)
    pdf.set_text_color(51, 65, 85)
    pdf.set_font("Helvetica", "", 8)
    
    row_count = min(len(df), 500)
    for i in range(row_count):
        row = df.iloc[i]
        
        # Zebra striping
        fill = (i % 2 == 0)
        if fill:
            pdf.set_fill_color(248, 250, 252)  # very light gray
        else:
            pdf.set_fill_color(255, 255, 255)

        for col in cols:
            val = row[col]
            # Clean display formatting
            if isinstance(val, (int, float)) and ("Gaji" in col or "Penjualan" in col or "Pagu" in col):
                val_str = f"Rp {val:,.0f}".replace(",", ".")
            elif isinstance(val, (datetime, pd.Timestamp)):
                val_str = val.strftime("%d-%m-%Y")
            else:
                val_str = str(val) if not pd.isna(val) else "-"
                
            # Truncate if too long to prevent overflow
            if len(val_str) > 22:
                val_str = val_str[:19] + "..."
                
            pdf.cell(col_width, 7, val_str, border=1, align="L", fill=True)
        pdf.ln()

    # Add message if truncated
    if len(df) > 500:
        pdf.ln(5)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 5, f"* Menampilkan 500 dari {len(df)} total baris data untuk optimalisasi ukuran dokumen.", ln=True, align="L")

    pdf.output(file_path)
    return file_path
