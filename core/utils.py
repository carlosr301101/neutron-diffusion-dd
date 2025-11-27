from math import exp
import numpy as np
def func_analitica(x):
    """Solución analítica de referencia"""
    return 1.705 * exp(-0.3 * x)

def calcular_desvios_relativos(valores_numericos, valores_analiticos):
    """Calcula desvíos relativos evitando división por cero"""
    desvios = np.abs((valores_numericos - valores_analiticos) / (np.abs(valores_analiticos) + 1e-10)) * 100
    return desvios