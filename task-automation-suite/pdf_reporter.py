"""
pdf_reporter.py — Generate styled PDF reports using fpdf2.

Produces a nicely formatted PDF with:
  - Header with title and timestamp
  - Summary statistics table
  - Body text sections
  - Footer with page numbers
"""

import os
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

REPORTS_DIR = Path("reports")

# Colour palette
DARK     = (15,  23,  42)   # near-black
ACCENT   = (37, 99,  235)   # blue
LIGHT_BG = (241, 245, 249)  # light grey-blue
WHITE    = (255, 255, 255)
GREY     = (100, 116, 139)


def _ensure_reports_dir():
    REPORTS_DIR.mkdir(exist_ok=True)


class StyledPDF(FPDF):
    def __init__(self, title: str):
        super().__init__()
        self.report_title = title
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Coloured header bar
        self.set_fill_color(*ACCENT)
        self.rect(0, 0, 210, 22, "F")
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*WHITE)
        self.set_y(6)
        self.cell(0, 10, self.report_title, align="C")
        # Timestamp on right
        self.set_font("Helvetica", "", 8)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.set_xy(140, 8)
        self.cell(55, 6, f"Generated: {ts}", align="R")
        self.ln(18)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GREY)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def section_title(self, text: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT)
        self.set_fill_color(*LIGHT_BG)
        self.cell(0, 8, f"  {text}", ln=True, fill=True)
        self.ln(2)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def key_value_table(self, rows: list[tuple[str, str]]):
        """Render a simple two-column key-value table."""
        col_w = [60, 115]
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*ACCENT)
        self.set_text_color(*WHITE)
        self.cell(col_w[0], 7, "  Field", fill=True)
        self.cell(col_w[1], 7, "  Value", fill=True, ln=True)

        for i, (key, val) in enumerate(rows):
            fill = i % 2 == 0
            self.set_fill_color(*LIGHT_BG if fill else WHITE)
            self.set_text_color(*DARK)
            self.set_font("Helvetica", "B", 9)
            self.cell(col_w[0], 6, f"  {key}", fill=fill)
            self.set_font("Helvetica", "", 9)
            self.cell(col_w[1], 6, f"  {val}", fill=fill, ln=True)
        self.ln(4)

    def data_table(self, headers: list[str], rows: list[list[str]]):
        """Render a multi-column data table."""
        n = len(headers)
        col_w = 175 // n

        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*ACCENT)
        self.set_text_color(*WHITE)
        for h in headers:
            self.cell(col_w, 7, f"  {h}", fill=True)
        self.ln()

        for i, row in enumerate(rows):
            fill = i % 2 == 0
            self.set_fill_color(*LIGHT_BG if fill else WHITE)
            self.set_text_color(*DARK)
            self.set_font("Helvetica", "", 9)
            for cell in row:
                self.cell(col_w, 6, f"  {str(cell)}", fill=fill)
            self.ln()
        self.ln(4)


def generate_report(
    title: str,
    sections: list[dict],
    filename: str = "",
) -> str:
    """
    Generate a PDF report.

    Args:
        title:    Report title shown in the header.
        sections: List of section dicts. Each dict has:
                    - 'heading': str  (section title)
                    - 'text':    str  (optional body paragraph)
                    - 'kv':      list[tuple[str,str]]  (optional key-value pairs)
                    - 'table':   dict with 'headers' and 'rows' (optional data table)
        filename: Output filename (without path). Auto-generated if blank.

    Returns:
        Absolute path to the saved PDF.
    """
    _ensure_reports_dir()

    pdf = StyledPDF(title)
    pdf.add_page()

    for section in sections:
        if heading := section.get("heading"):
            pdf.section_title(heading)
        if text := section.get("text"):
            pdf.body_text(text)
        if kv := section.get("kv"):
            pdf.key_value_table(kv)
        if table := section.get("table"):
            pdf.data_table(table["headers"], table["rows"])

    if not filename:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{ts}.pdf"

    out_path = REPORTS_DIR / filename
    pdf.output(str(out_path))
    return str(out_path)
