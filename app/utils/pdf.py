import pdfplumber

def ler_pdf(file):
    texto_total = ""

    with pdfplumber.open(file) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_total += texto + "\n"

    return texto_total
