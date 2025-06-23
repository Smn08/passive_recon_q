# ...existing code from export_report.py...

import csv
from fpdf import FPDF
from datetime import datetime
from rich import print
import os

def export_to_csv(results, filename):
    """Экспортирует результаты в CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for section, data in results.items():
            writer.writerow([section])
            if isinstance(data, list):
                for item in data:
                    writer.writerow(['', item])
            else:
                writer.writerow(['', data])
            writer.writerow([])

def export_to_pdf(results, target, filename):
    """Экспортирует результаты в PDF"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'OSINT Report for {target}', ln=True)
    pdf.set_font('Arial', '', 12)
    for section, data in results.items():
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, section, ln=True)
        pdf.set_font('Arial', '', 12)
        if isinstance(data, list):
            for item in data:
                pdf.cell(0, 8, f'- {item}', ln=True)
        else:
            pdf.multi_cell(0, 8, str(data))
        pdf.ln(2)
    pdf.output(filename)
