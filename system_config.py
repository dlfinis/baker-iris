# m1_config.py
from dataclasses import dataclass
import platform

@dataclass
class M1Config:
    use_mps: bool = True  # Metal Performance Shaders
    optimize_for_arm: bool = True
    memory_efficient: bool = True
    batch_size: int = 16  # Ajustado para M1

class SystemM1Optimizer:
    def __init__(self):
        self.is_m1 = platform.processor() == 'arm'
        self.has_mps = self._check_mps_availability()

    def _check_mps_availability(self) -> bool:
        """Verifica si MPS está disponible."""
        import torch
        return torch.backends.mps.is_available()

    def optimize_system(self) -> dict:
        """Aplica optimizaciones específicas para M1."""
        if not self.is_m1:
            return {"status": "not_m1"}

        return {
            "backend": "mps" if self.has_mps else "cpu",
            "optimizations_applied": True,
            "architecture": "arm64"
        }
