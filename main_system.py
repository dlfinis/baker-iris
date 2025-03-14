import torch
import platform
from typing import Optional

class InterviewSystemM1:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = self._setup_device()
        self.optimizer = TorchOptimizer()

    def _setup_device(self) -> torch.device:
        """Configura el dispositivo óptimo para M1."""
        if torch.backends.mps.is_available():
            print("Utilizando MPS (Metal Performance Shaders)")
            return torch.device("mps")
        print("Utilizando CPU")
        return torch.device("cpu")

    async def initialize_models(self):
        """Inicializa y optimiza los modelos para M1."""
        # Inicializar Whisper
        self.whisper_model = self._initialize_whisper()

        # Inicializar detector de preguntas
        self.question_detector = self._initialize_question_detector()

        # Optimizar modelos para M1
        self.whisper_model = self.optimizer.optimize_model(self.whisper_model)
        self.question_detector = self.optimizer.optimize_model(self.question_detector)

    def _initialize_whisper(self):
        """Inicializa Whisper optimizado para M1."""
        import whisper
        model = whisper.load_model(self.config.whisper_model)
        return model.to(self.device)
