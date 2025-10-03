import joblib
import sys

try:
    vec = joblib.load('tfidf.joblib')
    model = joblib.load('modelo.joblib')
    print('TFIDF features:', len(vec.get_feature_names_out()))
    Xn = vec.transform(['La compra fue excelente, todo perfecto'])
    pred = model.predict(Xn)[0]
    print('Predicción ejemplo:', 'positivo' if pred==1 else 'negativo')
except Exception as e:
    print('ERROR al cargar o predecir:', e)
    sys.exit(2)
