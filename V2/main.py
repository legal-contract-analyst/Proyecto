import pdfplumber
import re
import spacy

nlp = spacy.load("es_core_news_sm")

PDF_PATH = "contrato_ejemplo.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    texto = ""
    for page in pdf.pages:
        texto += page.extract_text() + "\n"
    

def limpiar_texto(texto):
    texto = re.sub(r'\n+',' ', texto)
    texto = re.sub(r'\s{2,}', ' ', texto)
    texto = re.sub(r'Página\s+\d+\s+de\s+\d+','', texto, flags=re.IGNORECASE)
    texto = re.sub(r'(PRIMERO | SEGUNDO | TERCERO | CUARTO)', r'\n\1', texto, flags=re.IGNORECASE)
    
    return texto.strip()

def analizar_texto(texto):
    doc = nlp(texto)
    for ent in doc.ents:
        print(ent.text,"->", ent.label_)

if __name__ == "__main__":
    ruta = "contrato_ejemplo.pdf"

    texto_crudo = texto
    texto_limpio = limpiar_texto(texto_crudo)


print("Textonormalizado:\n")
print(texto_limpio)

print("\n--- Entidades detectadas ---\n")
analizar_texto(texto_limpio)
