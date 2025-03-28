import subprocess
import sys
import spacy

def install_spacy():
    """Verifica e instala SpaCy si no está disponible."""
    try:
        import spacy
        print("✅ SpaCy ya está instalado.")
    except ModuleNotFoundError:
        print("⚠️ SpaCy no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
        print("✅ SpaCy instalado correctamente.")

def download_spacy_models():
    """Descarga los modelos necesarios de SpaCy."""
    try:
        print("✅ Descargando modelos de SpaCy...")
        spacy.cli.download("en_core_web_sm")
        spacy.cli.download("es_core_news_sm")
        print("✅ Modelos de SpaCy descargados correctamente.")
    except Exception as e:
        print(f"❌ Error descargando modelos de SpaCy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_spacy()
    download_spacy_models()