import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import tempfile, os


SRATE = 16000     # tasa de muestreo
DUR = 5           # segundos

print("Grabando... habla ahora!")
audio = sd.rec(int(DUR*SRATE), samplerate=SRATE, channels=1, dtype='int16')
sd.wait()
print("Listo, procesando...")

# guarda a WAV temporal
tmp_wav = tempfile.mktemp(suffix=".wav")
write(tmp_wav, SRATE, audio)

# reconoce con SpeechRecognition
r = sr.Recognizer()
with sr.AudioFile(tmp_wav) as source:
    data = r.record(source)

try:
    texto = r.recognize_google(data, language="es-ES")
    print("Dijiste:", texto)
except sr.UnknownValueError:
    print("No se entendió el audio.")
except sr.RequestError as e:
    print("Error:", e)
finally:
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)

cmd = texto.lower()

if "hola" in cmd:
    print("¡Hola, bienvenido al curso!")
elif "abrir google" in cmd:
    import webbrowser
    webbrowser.open("https://www.google.com")
elif "hora" in cmd:
    from datetime import datetime
    print("Hora actual:", datetime.now().strftime("%H:%M"))
elif "clima" in cmd:
    import requests
    try:
        # obtener ciudad según IP
        data = requests.get("https://ipinfo.io/json").json()
        ciudad = data.get("city")

        if ciudad:
            # pedir clima de esa ciudad
            resp = requests.get(f"https://wttr.in/{ciudad}?format=3")
            if resp.status_code == 200:
                print(f"Clima actual en {ciudad}: {resp.text}")
            else:
                print("No se pudo obtener el clima.")
        else:
            print("No pude detectar tu ciudad.")
    except Exception as e:
        print("Error al consultar el clima:", e)

elif "youtube" in cmd:
    import webbrowser, urllib.parse
    busqueda = cmd.replace("youtube", "").strip()
    if busqueda:
        query = urllib.parse.quote(busqueda)
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    else:
        webbrowser.open("https://www.youtube.com")
elif "ubicación" in cmd:
    import webbrowser, requests
    try:
        data = requests.get("https://ipinfo.io/json").json()
        ciudad = data.get("city")
        pais = data.get("country")
        if ciudad and pais:
            print(f"Según mi información, estás en {ciudad}, {pais}. ¿Es correcto? (sí/no)")
            respuesta = input("> ").strip().lower()
            if respuesta in ["si", "sí", "yes", "y"]:
                print("¡Perfecto!")
            else:
                print("Lo siento por la confusión, abriendo Google Maps...")
                webbrowser.open("https://www.google.com/maps")
        else:
            print("No pude detectar la ciudad. Abriendo Google Maps...")
            webbrowser.open("https://www.google.com/maps")
    except Exception as e:
        print("Error al obtener la ubicación, abriendo Google Maps...")
        webbrowser.open("https://www.google.com/maps")
else:
    print("Comando no reconocido.")