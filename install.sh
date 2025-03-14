# install_m1_conda.sh
#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

ENV_NAME="baker-iris"
PYTHON_VERSION="3.9"

echo "🚀 Iniciando instalación para Apple Silicion utilizando conda..."

# Verificar e instalar Miniforge si no está presente
if ! command -v conda &> /dev/null; then
    echo "${RED}Conda no encontrado. Instalando Miniforge...${NC}"

    # Descargar el instalador de Miniforge
    echo "📥 Descargando Miniforge..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Para MacOS
        curl -LO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
        INSTALLER="Miniforge3-MacOSX-arm64.sh"
    else
        echo "${RED}Este script está diseñado para MacOS. Por favor, adapte el script para otros sistemas operativos.${NC}"
        exit 1
    fi

    # Ejecutar el instalador
    echo "🔧 Ejecutando el instalador de Miniforge..."
    bash $INSTALLER -b

    # Eliminar el instalador
    rm $INSTALLER

    # Inicializar conda para el shell actual
    echo "🔄 Inicializando conda..."
    eval "$($HOME/miniforge3/bin/conda shell.bash hook)"

    echo "${GREEN}✅ Miniforge se ha instalado correctamente!${NC}"
else
    echo "${GREEN}Conda ya está instalado.${NC}"
fi

# Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
if ! command -v brew &> /dev/null; then
    echo "${RED}Homebrew no encontrado. Instalando...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
brew install ffmpeg
brew install portaudio
brew install cmake

# Función para verificar si el entorno existe
check_conda_env_exists() {
    conda env list | grep -w "$ENV_NAME" &> /dev/null
}

echo "🔍 Verificando si el entorno conda '$ENV_NAME' ya existe..."

if check_conda_env_exists; then
    echo "${GREEN}✅ El entorno '$ENV_NAME' ya existe.${NC}"
    conda init
else
    echo "${RED}❌ El entorno '$ENV_NAME' no existe. Creando el entorno...${NC}"
    conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y
    conda init
fi

# Activar el entorno
echo "🔄 Activando el entorno conda '$ENV_NAME'..."
conda activate "$ENV_NAME"

echo "${GREEN}✅ El entorno '$ENV_NAME' está ahora activo.${NC}"

echo "📚 Instalando Tensorflow..."
conda install -c apple tensorflow-deps -y

# Instalar PyTorch para Apple Silicon
echo "📚 Instalando PyTorch y otras dependencias..."
conda install -c pytorch-nightly -c nvidia pytorch torchvision torchaudio -y

# Instalar otras dependencias específicas para Apple Silicon
pip install --upgrade pip

pip install \
    numpy \
    tensorflow-macos \
    tensorflow-metal \
    whisper-openai \
    spacy \
    transformers \
    sounddevice \
    pyaudio \
    librosa

echo "${GREEN}✅ Instalación completada!${NC}"
