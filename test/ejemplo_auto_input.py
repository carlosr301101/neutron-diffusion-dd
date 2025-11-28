"""
EJEMPLO DE USO: Config.auto_input - Cargando configuración desde diccionario
============================================================================

Este archivo muestra cómo utilizar la clase Config con la función auto_input()
para cargar toda la configuración del algoritmo de transporte desde un diccionario,
sin necesidad de inputs interactivos.

Estructura del diccionario:
---------------------------
El diccionario debe contener las siguientes claves:

    {
        'num_regions': int,                          # Número de regiones
        'num_zones': int,                            # Número de zonas de material
        'NC': list o np.array,                       # Celdas por región
        'HR': list o np.array,                       # Espesor total por región (cm)
        'IZL': list o np.array,                      # Zona asignada a cada región (1-based)
        'SCT': list o np.array,                      # Sigma total por zona
        'SCS': list o np.array,                      # Sigma scattering por zona
        'Q': list o np.array,                        # Fuente por región
        'N': int                                     # Orden de cuadratura (debe ser par)
        'reflex_izq': True,                          # Dice si es reflexivo izq   
        'reflex_der': False,                         # Dice si es reflexivo izq
        'bound_left': [0,0],                         # Valores de la fuente por la izq   
        'bound_right': [0,0]                         # Valores de la fuente por la der
    }

Ejemplo 1: Configuración simple (1 región, 1 zona)
===================================================
"""

import core.algoritm as alg

# Diccionario de configuración
config_simple = {
    'num_regions': 1,
    'num_zones': 1,
    'NC': [100],                    # 100 celdas
    'HR': [100.0],                  # Espesor total: 100 cm
    'IZL': [1],                     # La región 1 usa la zona 1
    'SCT': [1.0],                   # Sigma total = 1.0 cm^-1
    'SCS': [0.97],                  # Sigma scattering = 0.97 cm^-1
    'Q': [1.0],                     # Fuente = 1.0
    'N': 2                          # S2 cuadratura
}

# Crear Config sin inputs manuales
config = alg.Config(manual=False, reflexiva=True, **config_simple)

print("Configuración cargada:")
print(f"  Celdas totales: {config.NTC}")
print(f"  Nodos totales: {config.NTP}")
print(f"  Cuadratura: S{config.N}")

# Ejemplo 2: Configuración con múltiples regiones y zonas
# ======================================================
config_multi = {
    'num_regions': 2,
    'num_zones': 2,
    'NC': [50, 50],                 # 50 celdas en cada región
    'HR': [50.0, 50.0],             # 50 cm de espesor cada una
    'IZL': [1, 2],                  # Región 1 → Zona 1, Región 2 → Zona 2
    'SCT': [1.0, 2.0],              # Sigma totales diferentes
    'SCS': [0.97, 0.98],            # Sigma scattering diferentes
    'Q': [1.0, 0.5],                # Fuentes diferentes
    'N': 2
}

# Crear Config multi-región
config2 = alg.Config(manual=False, reflexiva=False, **config_multi)

print("\nConfiguración multi-región cargada:")
print(f"  Regiones: {config2.num_regions}")
print(f"  Zonas: {config2.num_zones}")
print(f"  Celdas totales: {config2.NTC}")

# Ejemplo 3: Usar Config en un cálculo completo
# ===============================================

# Crear Runner
runner = alg.Runner(config)

# Ejecutar cálculo
resultado = runner()
flujo_escalar = resultado[0]
num_iteraciones = resultado[1]

print("\nResultados de la simulación:")
print(f"  Iteraciones: {num_iteraciones}")
print(f"  Convergido: {runner.converged}")
print(f"  Flujo promedio (primeras 5 celdas): {flujo_escalar[:5]}")

# Ventajas de usar auto_input:
# ============================
# 1. No requiere inputs interactivos (ideal para scripts batch)
# 2. Fácil de reproducir estudios numéricos
# 3. Permite paralelización de múltiples configuraciones
# 4. Perfectamente integrable en workflows de análisis de sensibilidad
