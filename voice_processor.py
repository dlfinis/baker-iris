import webrtcvad
import sounddevice as sd
import numpy as np
from groq import Groq
import time
import queue
import struct
import wave
import io
import os
from dotenv import load_dotenv
from groq import Groq
from question_detector import QuestionDetector, QuestionAnalysis

load_dotenv()


# Configuración principal
SAMPLE_RATE = 16000  # Requerido por WebRTC VAD
CHANNELS = 1
FRAME_DURATION = 30  # ms
AGGRESSIVENESS = 1   # Nivel de detección (0-3)
MIN_UTTERANCE = 1.7   # Segundos mínimos de voz
SILENCE_TIMEOUT = 1.3 # Segundos para finalizar pregunta

class VoiceProcessor:
    def __init__(self):
        self.vad = webrtcvad.Vad(AGGRESSIVENESS)
        self.audio_buffer = bytearray()
        self.last_voice_time = time.time()
        self.sample_queue = queue.Queue()
        self.recording = False
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.whisper_model = os.getenv('WHISPER_MODEL_NAME')
        self.model = os.getenv('MODEL_NAME')
        
        # Cálculo de tamaños
        self.frame_size = int(SAMPLE_RATE * FRAME_DURATION / 1000)
        self.min_samples = int(SAMPLE_RATE * MIN_UTTERANCE)

    def audio_callback(self, indata, frames, time, status):
        """Callback para captura de audio en tiempo real"""
        # Convertir a PCM 16-bit
        pcm_data = (indata * 32767).astype(np.int16).tobytes()
        self.sample_queue.put(pcm_data)

    def process_audio(self):
        """Procesamiento principal del audio"""
        voice_frames = bytearray()
        silence_frames = 0
        required_silence = int(SILENCE_TIMEOUT * 1000 / FRAME_DURATION)

        while True:
            try:
                frame = self.sample_queue.get(timeout=1)
            except queue.Empty:
                continue

            # Detección de actividad vocal
            if self.vad.is_speech(frame, SAMPLE_RATE):
                voice_frames.extend(frame)
                silence_frames = 0
                if not self.recording:
                    self.recording = True
                    print("\n🔊 Voz detectada - Iniciando grabación...")
            else:
                if self.recording:
                    silence_frames += 1
                    if silence_frames >= required_silence:
                        if len(voice_frames) >= self.min_samples * 2:  # 16-bit = 2 bytes
                            self.process_question(voice_frames)
                        voice_frames = bytearray()
                        silence_frames = 0
                        self.recording = False
                        print("🛑 Silencio detectado - Procesando pregunta...")

    def create_wav_buffer(self, pcm_data):
        """Crea un buffer WAV válido desde datos PCM"""
        with io.BytesIO() as wav_buffer:
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(CHANNELS)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(SAMPLE_RATE)
                wav_file.writeframes(pcm_data)
            return wav_buffer.getvalue()

    def process_question(self, audio_data):
        """Procesa el audio y genera respuesta"""
        detector = QuestionDetector()
        try:
            # Crear archivo WAV en memoria
            wav_data = self.create_wav_buffer(audio_data)
            
            # Transcribir con Whisper
            transcript = self.client.audio.transcriptions.create(
                file=("pregunta.wav", wav_data, "audio/wav"),
                model=self.whisper_model,
                language="es"
            )
            content = transcript.text
            print(f"\n🎤 Transcripcion: {content}")
            #questions = detector.analyze_text(content)
            
            #for question_analysis in questions:
             #   print(f"\n🔍 Análisis de pregunta: {question_analysis}")
                # Generar respuesta considerando el análisis
              #  self.generate_response(question_analysis)
                ##self._output_response_with_analysis(question_analysis, response)
                
            
            #prompt = self._build_prompt(question)
            print(f"\n🎤 Pregunta detectada: {content}")
            
            # Generar respuesta
            self.generate_response(content)
            
        except Exception as e:
            print(f"❌ Error en procesamiento: {str(e)}")

    def generate_response(self, question):
        """Genera respuesta usando el LLM"""
        try:
            respuesta = self.client.chat.completions.create(
                model=self.model,
                messages=[
                   {"role": "system", "content": "Eres un asistente para entrevistas profesionales de desarrollador de sistemas enfocado en Java, servicios web, aws, design of system, arquitectura de sistemas."},
                   {"role": "user", "content": question}
                ],
                max_tokens=150,
                temperature=0.5
            )
            print(f"\n🤖 Asistente: {respuesta.choices[0].message.content}\n")
            
        except Exception as e:
            print(f"❌ Error generando respuesta: {str(e)}")

    def _build_prompt(self, question_analysis: QuestionAnalysis) -> str:
        """Construye el prompt para Groq."""
        return f"""
            Tipo de pregunta: {question_analysis.question_type.value if question_analysis.question_type else 'General Desarrollo'}
            Complejidad: {question_analysis.complexity}
            Contexto: {question_analysis.context if question_analysis.context else 'No disponible'}
            Palabras clave: {', '.join(question_analysis.keywords)}

            Pregunta: {question_analysis.text}

            Por favor, proporciona una respuesta clara y concisa, considerando el tipo y la complejidad de la pregunta.
            """

    def _output_response(self, 
                        question_analysis: QuestionAnalysis, 
                        response: str):
        """Muestra la pregunta y su respuesta."""
        print("\n" + "="*50)
        print(f"Pregunta detectada: {question_analysis.text}")
        print(f"Tipo: {question_analysis.question_type.value}")
        print(f"Confianza: {question_analysis.confidence:.2f}")
        print(f"Complejidad: {question_analysis.complexity}")
        print(f"Respuesta: {response}")
        print("="*50 + "\n")
def main():
    processor = VoiceProcessor()
    
    # Configurar dispositivo de audio
    print("🎧 Inicializando sistema de entrevistas...")
    print("✅ Configuración lista")
    print("🔊 Escuchando... (Presiona Ctrl+C para detener)")
    
    try:
        with sd.InputStream(
            callback=processor.audio_callback,
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            blocksize=processor.frame_size
        ):
            processor.process_audio()
    except KeyboardInterrupt:
        print("\n🔴 Sistema detenido")

if __name__ == "__main__":
    main()