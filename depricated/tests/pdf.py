import pdfplumber
import os

texto_total = ""
with pdfplumber.open(os.getcwd() +"/parser/eros_psique.pdf") as pdf:
    for pagina in pdf.pages:
        texto_total += pagina.extract_text() + "\n"

# print(texto_total)
