import re, random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

random.seed(42); np.random.seed(42)

positivos = [
    "Excelente servicio","Muy buena atención","Me encantó el producto",
    "Rápido y confiable","Todo llegó perfecto","Calidad superior",
    "Lo recomiendo totalmente","Volveré a comprar","Precio justo y buena calidad",
    "El soporte fue amable","Experiencia increíble","Funcionó mejor de lo esperado",
    "Entregado a tiempo","Muy satisfecho","Cinco estrellas",
    "La comida estaba deliciosa","El empaque impecable","Súper recomendable",
    "Buen trato del personal","Gran experiencia"
]

negativos = [
    "Pésimo servicio","Muy mala atención","Odio este producto",
    "Lento y poco confiable","Llegó dañado","Calidad terrible",
    "No lo recomiendo","No vuelvo a comprar","Caro y mala calidad",
    "El soporte fue grosero","Experiencia horrible","Peor de lo esperado",
    "Entregado tarde","Muy decepcionado","Una estrella",
    "La comida estaba fría","El empaque roto","Nada recomendable",
    "Mal trato del personal","Mala experiencia"
]

def variantes(frase):
    extras = ["", "!", "!!", " 🙂", " 😡", " de verdad", " en serio", " 10/10", " 1/10",
              " súper", " la verdad", " jamás", " nunca", " para nada"]
    return frase + random.choice(extras)

pos = [variantes(p) for _ in range(8) for p in positivos]
neg = [variantes(n) for _ in range(8) for n in negativos]
textos = pos + neg
etiquetas = [1]*len(pos) + [0]*len(neg)

df = pd.DataFrame({"texto": textos, "etiqueta": etiquetas}).sample(frac=1, random_state=42).reset_index(drop=True)

def limpiar(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-záéíóúñü0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

df["texto_clean"] = df["texto"].apply(limpiar)

# Guardar dataset para inspección/uso en producción
df.to_csv("dataset.csv", index=False, encoding="utf-8")
print(f"Dataset guardado: dataset.csv ({df.shape[0]} filas)")

# Entrenar TF-IDF sobre todo el dataset (vocabulario que se usará en producción)
vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1,2), min_df=2)
X = vectorizer.fit_transform(df["texto_clean"])

# Guardar vocabulario + idf a un archivo legible
features = vectorizer.get_feature_names_out()
idf = vectorizer.idf_
with open("tfidf_features.txt", "w", encoding="utf-8") as f:
    f.write("feature\tindex\tidf\n")
    for idx, (feat, val) in enumerate(zip(features, idf)):
        f.write(f"{feat}\t{idx}\t{val}\n")

print(f"TF-IDF features guardadas: tfidf_features.txt (n_features={len(features)})")

# Adicional: guardar el vectorizer con joblib para uso en producción
try:
    import joblib
    joblib.dump(vectorizer, "tfidf.joblib")
    print("Vectorizer guardado en tfidf.joblib")
except Exception:
    print("joblib no está disponible; no se guardó tfidf.joblib")
