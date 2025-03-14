# verify_apple_silicon_setup.py
import torch
import platform

def verify_m1_setup():
    print(f"Arquitectura: {platform.processor()}")
    print(f"MPS disponible: {torch.backends.mps.is_available()}")
    print(f"Dispositivo actual: {torch.device('mps' if torch.backends.mps.is_available() else 'cpu')}")

verify_m1_setup()
