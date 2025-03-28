import os
import subprocess
import sys

def install_package(package_name):
    """Instala un paquete si no está disponible."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Paquete '{package_name}' instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando el paquete '{package_name}': {e}")
        sys.exit(1)

def ensure_package_installed(package_name, import_name=None):
    """Verifica si un paquete está instalado; si no, lo instala."""
    try:
        if import_name is None:
            import_name = package_name
        __import__(import_name)
        print(f"✅ Paquete '{package_name}' ya está instalado.")
    except ModuleNotFoundError:
        print(f"⚠️ Paquete '{package_name}' no está instalado. Instalando...")
        install_package(package_name)

# Asegúrate de que las dependencias críticas estén instaladas
ensure_package_installed("python-dotenv", "dotenv")
ensure_package_installed("spacy")

# Ahora importa las dependencias necesarias
from dotenv import load_dotenv
from setup_spacy import install_spacy, download_spacy_models

def check_and_install_dependencies():
    """Verifica e instala las dependencias necesarias."""
    try:
        print("✅ Verificando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        sys.exit(1)

def setup_environment():
    """Configura el entorno cargando variables de entorno y modelos."""
    print("✅ Configurando entorno...")
    load_dotenv()  # Carga las variables de entorno desde .env
    install_spacy()  # Verifica e instala SpaCy si es necesario
    download_spacy_models()  # Descarga los modelos de SpaCy
    print("✅ Entorno configurado correctamente.")

if __name__ == "__main__":
    print("🔧 Iniciando configuración inicial del proyecto...")
    check_and_install_dependencies()
    setup_environment()
    print("✅ Configuración inicial completada.")