# performance_tuning_m1.py
class M1PerformanceTuner:
    def __init__(self):
        self.memory_efficient = True
        self.batch_size = 16  # Optimizado para M1

    def optimize_memory_usage(self):
        """Optimiza el uso de memoria para M1."""
        import torch
        torch.set_num_threads(6)  # Ajustar según núcleos disponibles

        if torch.backends.mps.is_available():
            # Configuraciones específicas para MPS
            torch.backends.mps.enable_fallback_warnings = False
