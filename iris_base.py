import sounddevice as sd
import numpy as np
import queue
import io
import wave
import threading
import os
import time
import keyboard
from dotenv import load_dotenv
from groq import Groq


# Configuración
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = 'int16'
API_KEY = os.getenv("GROQ_API_KEY")

class RecordingController:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.whisper_model = os.getenv('WHISPER_MODEL_NAME')
        self.model = os.getenv('MODEL_NAME')
        self.audio_buffer = np.array([], dtype=np.int16) 
        self.is_recording = False
        self.lock = threading.Lock()
        self.input_queue = queue.Queue()
        self.stream = None

    def start_audio_stream(self):
        """Inicia el stream de audio"""
        self.stream = sd.InputStream(
            callback=self.audio_callback,
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            dtype=FORMAT
        )
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        """Callback que se ejecuta constantemente para capturar audio"""
        with self.lock:
            if self.is_recording:
                flattened = indata.flatten().astype(np.int16)
                self.audio_buffer = np.concatenate((self.audio_buffer, flattened))

    def toggle_recording(self):
        """Alterna entre iniciar/detener grabación"""
        with self.lock:
            if self.is_recording:
                # Detener grabación y procesar
                self.process_audio()
                self.is_recording = False
                print("\n⏹️  Detener grabacion - Procesando...")
            else:
                # Iniciar nueva grabación
                self.audio_buffer = np.array([], dtype=FORMAT)
                self.is_recording = True
                print("\n⏺️  Grabación iniciada... ¡Habla!")

    def create_wav(self):
        """Crea archivo WAV en memoria desde el buffer"""
        with io.BytesIO() as wav_buffer:
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(CHANNELS)
                wav_file.setsampwidth(2)
                wav_file.setframerate(SAMPLE_RATE)
                wav_file.writeframes(self.audio_buffer.tobytes())
            return wav_buffer.getvalue()

    def process_audio(self):
        """Procesa el audio grabado"""
        try:
            if len(self.audio_buffer) == 0:
                print("⚠️  No hay audio grabado")
                return

            # Convertir a WAV
            wav_data = self.create_wav()
            
            # Transcribir con Whisper
            transcript = self.client.audio.transcriptions.create(
                file=("grabacion.wav", wav_data, "audio/wav"),
                model=self.whisper_model,
                language="en"
            )
            print(f"\n📝 Transcripción: {transcript.text}")
            
            # Generar respuesta
            self.generate_response(transcript.text)

        except Exception as e:
            print(f"❌ Error procesando audio: {str(e)}")

    def generate_response(self, text):
        """Genera respuesta usando el LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un asistente especializado en apoyar entrevistas para desarrolladores de sistemas de nivel semi senior, con enfoque en Java, servicios web, AWS, arquitectura de sistemas y sistemas reactivos. Responde de manera concisa, usando un máximo de 3 líneas, en el idioma predominante de la pregunta. Si encuentras una palabra desconocida, interpreta su significado utilizando el contexto."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200,
                temperature=0.5
            )
            print(f"\n🤖 Respuesta: {response.choices[0].message.content}\n")
        except Exception as e:
            print(f"❌ Error generando respuesta: {str(e)}")

def input_handler(controller):
    """Maneja la entrada del usuario"""
    print("\nControles:")
    print("  s: Iniciar/Detener grabación")
    print("  q: Salir\n")
    
    while True:
        #cmd = input("Comando: ").lower()
        #if cmd == 's':
        if keyboard.is_pressed('s'):
            controller.toggle_recording()
            time.sleep(0.5)
        elif keyboard.is_pressed('q'):
            print("\n🔴 Apagando sistema...")
            controller.stream.stop()
            exit()

def main():
    controller = RecordingController()
    controller.start_audio_stream()

    # Hilo para entrada de usuario
    input_thread = threading.Thread(
        target=input_handler,
        args=(controller,),
        daemon=True
    )
    input_thread.start()

    # Mantener el programa activo
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        controller.stream.stop()
        print("\n🔴 Sistema detenido")

if __name__ == "__main__":
    main()