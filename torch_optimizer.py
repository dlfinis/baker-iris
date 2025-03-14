# torch_m1_optimizer.py
import torch

class TorchOptimizer:
    def __init__(self):
        self.device = self._get_optimal_device()

    def _get_optimal_device(self):
        """Determina el mejor dispositivo disponible para M1."""
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")

    def optimize_model(self, model):
        """Optimiza un modelo para M1."""
        model = model.to(self.device)
        # Activar optimizaciones específicas de M1
        if self.device.type == "mps":
            model = torch.compile(model)
        return model
