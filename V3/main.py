import pdfplumber
import re
import spacy

nlp = spacy.load("es_core_news_sm")

PDF_PATH = "contrato_ejemplo.pdf"

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

def detectar_clausulas(texto):
    resultados = {}

    fechas = re.findall(r'\b(\d{1,2}\s+de\s+[A-Za-záéíóú]+(?:\s+de)?\s+\d{4})\b', texto, flags=re.IGNORECASE)
    fechas += re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b', texto)
    resultados["Fechas"] = list(set(fechas))

    montos = re.findall(r'(\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?)', texto)
    montos += re.findall(r'(\d+\s?UF)', texto, flags=re.IGNORECASE)
    montos += re.findall(r'(US\$?\s?\d+(?:,\d{1,2})?)', texto, flags=re.IGNORECASE)
    resultados["Montos"] = list(set(montos))

    partes = re.findall(r'(Don\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)', texto)
    partes += re.findall(r'(Doña\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)', texto)
    partes += re.findall(r'([A-Z][A-Za-z&\s]+(?:Ltda\.|SpA|S\.A\.))', texto)
    resultados["Partes"] = list(set(partes))

    jurisdicciones = re.findall(r'(Santiago|Valparaíso|Quilpué|Villa Alemana|Limache|Los Andes|Viña del mar|Concepción|Chile|República de Chile)', texto, flags=re.IGNORECASE)
    resultados["Jurisdicción"] = list(set(jurisdicciones))

    return resultados

if __name__ == "__main__":
    PDF_PATH = "contrato_ejemplo.pdf"

    with pdfplumber.open(PDF_PATH) as pdf: 
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() + "\n"

    texto_limpio = limpiar_texto(texto)


    print("Textonormalizado:\n")
    print(texto_limpio)
    
    print("\n--- Entidades detectadas ---\n")
    analizar_texto(texto_limpio)

    print("\n---Información clave extraída ---\n")
    clausulas = detectar_clausulas(texto_limpio)
    for categoria, items in clausulas.items():
        print(f"{categoria}:")
        for i in items:
            print("   -", i)
