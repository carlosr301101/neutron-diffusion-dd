import core.algoritm as alg
import matplotlib.pyplot as plt
import numpy as np
from math import exp
import pandas as pd

def func_analitica(x):
    """Solución analítica de referencia"""
    return 1.705 * exp(-0.3 * x)

def calcular_desvios_relativos(valores_numericos, valores_analiticos):
    """Calcula desvíos relativos evitando división por cero"""
    desvios = np.abs((valores_numericos - valores_analiticos) / (np.abs(valores_analiticos) + 1e-10)) * 100
    return desvios

def run():
    config = alg.Config(manual=True)
    runner1 = alg.Runner(config)
    valores_flujo, n_iter = runner1()
    
    malla = len(valores_flujo)
    h = 100 // malla
    
    # Calcular coordenadas de las celdas (centros)
    x_celdas = np.arange(malla) * h + h/2
    valores_analiticos = np.array([func_analitica(x) for x in x_celdas])
    
    # Calcular desvíos relativos
    desvios_relativos = calcular_desvios_relativos(valores_flujo, valores_analiticos)
    
    # Crear figura con 2 subgráficas (lado a lado)
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    
    # Gráfica 1: Comparación de valores numéricos vs analíticos
    axes[0].plot(x_celdas, valores_analiticos, color='green', linewidth=2, label='Solución analítica')
    axes[0].scatter(x_celdas, valores_flujo, color='blue', s=20, alpha=0.6, label='Solución numérica (Diamond Difference)')
    axes[0].set_xlabel('Posición x (cm)')
    axes[0].set_ylabel('Flujo escalar')
    axes[0].set_title(f'Comparación: Solución Numérica vs Analítica (Malla: {malla} celdas, Iteraciones: {n_iter})')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Gráfica 2: Desvío relativo
    axes[1].semilogy(x_celdas, desvios_relativos, color='red', marker='o', markersize=4, linewidth=1.5)
    axes[1].set_xlabel('Posición x (cm)')
    axes[1].set_ylabel('Desvío relativo (%)')
    axes[1].set_title('Desvío Relativo del Flujo Escalar')
    axes[1].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig("comparacion_flujos.png", dpi=150)
    print("✓ Gráfica guardada como: comparacion_flujos.png")
    plt.show()
    
    # Mostrar estadísticas
    print(f"\n{'='*60}")
    print("ESTADÍSTICAS DE CONVERGENCIA")
    print(f"{'='*60}")
    print(f"Número de iteraciones: {n_iter}")
    print(f"Número de celdas: {malla}")
    print(f"Espesor de celda: {h} cm")
    print(f"Desvío relativo máximo: {np.max(desvios_relativos):.6f}%")
    print(f"Desvío relativo medio: {np.mean(desvios_relativos):.6f}%")
    print(f"Desvío relativo mínimo: {np.min(desvios_relativos):.6f}%")
    print(f"{'='*60}\n")
    
    # Guardar resultados en CSV
    resultados = pd.DataFrame({
        'x_celda': x_celdas,
        'flujo_numerico': valores_flujo,
        'flujo_analitico': valores_analiticos,
        'desvio_relativo_%': desvios_relativos
    })
    resultados.to_excel("resultados_comparacion.xlsx", index=False)
    print("✓ Resultados guarto_dados como: resultados_comparacion.csv")

if __name__ == "__main__":
    run()

