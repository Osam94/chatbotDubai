import fitz  # pymupdf
import pandas as pd
import re

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    rows = []
    pattern = re.compile(r'(\d+)\s+(\d{8,}-\d+)(.*?)\s+(\d{12,})\s+(\d+)\s+(\d+)', re.DOTALL)
    for match in pattern.finditer(text):
        rows.append({
            "№": match.group(1),
            "Номер отправления": match.group(2),
            "Товар": match.group(3).strip(),
            "Артикул": match.group(4),
            "Кол-во": match.group(5),
            "Этикетка": match.group(6),
        })

    return pd.DataFrame(rows)
