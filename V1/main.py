import pdfplumber
import spacy

nlp = spacy.load("es_core_news_sm")

PDF_PATH = "contrato_ejemplo.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    texto = ""
    for page in pdf.pages:
        texto += page.extract_text() + "\n"

print("Texto del contrato: \n")
print(texto)

doc = nlp(texto)

print("\nEntidades detectadas:\n")
for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")