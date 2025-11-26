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

config_dict = {
    'num_regions': 3,
    'num_zones': 3,
    'NC': [10,30,10],                  
    'HR': [10,30,10],                  
    'IZL': [1,2,3],                     
    'SCT': [1.0,0.6,1],                   
    'SCS': [0.99,0.4,0.9],                  
    'Q': [2,0,0],                     
    'N': 4                       
}


config_dict_fino = {
    'num_regions': 3,
    'num_zones': 3,
    'NC': [20,60,20],                    
    'HR': [10,30,10],                  
    'IZL': [1,2,3],                     
    'SCT': [1.0,0.6,1],                   
    'SCS': [0.99,0.4,0.9],                  
    'Q': [2,0,0],                     
    'N': 4                    
}

def run():
    config = alg.Config(manual=False,reflexiva=True,**config_dict)
    runner1 = alg.Runner(config)
    
    config_fino= alg.Config(manual=False, reflexiva=True, **config_dict_fino)
    runner_fino= alg.Runner(config_fino)
    
    valores_flujo_fino, n_iter_fino,right_flux_fino,left_flux_fino = runner_fino() # Aqui ocurren los calculos
    
    
    valores_flujo, n_iter,right_flux,left_flux = runner1() # Aqui ocurren los calculos
    x_fino= np.arange(0,sum(config_fino.HR),0.5)
    
    print(right_flux,left_flux)
    print(len(right_flux),len(left_flux))
    malla = len(valores_flujo)
    h = sum(config.HR) / malla
    print(malla,config.NTC)
    # Calcular coordenadas de las celdas (centros)
    x_celdas = np.arange(malla) * h + h/2
    # valores_analiticos = np.array([func_analitica(x) for x in x_celdas]) # Flujo analitico para EX1
    
    
    # Calcular desvíos relativos
    step=2 # Cambiar el step para graficar la misma cantidad de datos de ambas mallas
    desvios_relativos = calcular_desvios_relativos(valores_flujo, valores_flujo_fino[::step])
    
    # Crear figura con 2 subgráficas (lado a lado)
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    
    # Gráfica 1: Comparación de valores numéricos vs analíticos
    # axes[0].plot(x_celdas, valores_analiticos, color='green', linewidth=2, label='Solución analítica')
    axes[0].scatter(x_celdas, valores_flujo, color='blue', s=20, alpha=0.6, label='Solución numérica')
    axes[0].set_xlabel('Posición x (cm)')
    axes[0].set_ylabel('Flujo escalar [n/m^2-s]')
    axes[0].set_title(f'Comparación: Solución Numérica(Malla: {malla} celdas, Iteraciones: {n_iter})')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Gráfica 2: Desvío relativo
    axes[1].semilogy(x_celdas, desvios_relativos, color='red', marker='o', markersize=4, linewidth=1.5)
    axes[1].set_xlabel('Posición x (cm)')
    axes[1].set_ylabel('Desvío relativo (%) logarítmico')
    axes[1].set_title('Desvío Relativo del Flujo Escalar')
    axes[1].grid(True, alpha=0.3, which='both')
    print(len(x_celdas),len(valores_flujo_fino))
  
    #Comparar los flujos
    
    # axes[1].scatter(x_celdas, valores_flujo, color='blue', s=20, alpha=0.6, label='Solución numérica')
    # axes[1].scatter(x_fino, valores_flujo_fino, color='red', s=20, alpha=0.6, label='Solución numérica FINA')
    
    # axes[1].set_xlabel('Posición x (cm)')
    # axes[1].set_ylabel('Flujo escalar [n/m^2-s]')
    # axes[1].set_title(f'Comparación: Flujos Escalares (Malla: {malla} celdas, Iteraciones: {n_iter})')
    # axes[1].grid(True, alpha=0.3)
    # axes[1].legend()
    
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
    print(f"Espesor de celda: {sum(config.HR)/malla} cm")
    print(f"Desvío relativo máximo: {np.max(desvios_relativos):.6f}%")
    print(f"Desvío relativo medio: {np.mean(desvios_relativos):.6f}%")
    print(f"Desvío relativo mínimo: {np.min(desvios_relativos):.6f}%")
    print(f"{'='*60}\n")
    
    # Guardar resultados en CSV
    resultados = pd.DataFrame({
        'x_celda': x_celdas,
        'flujo_numerico': valores_flujo,
        'flujo_numerico_fino': valores_flujo_fino[::step],
        'desvio_relativo_%': desvios_relativos
    })
    resultados.to_excel("resultados_comparacion.xlsx", index=False)
    print("✓ Resultados guarto_dados como: resultados_comparacion.csv")
    
    x1=int(10/h)
    x2=int(25/h)
    x3=int(40/h)
    print(h)
    data= pd.read_csv("EX1_data.csv")
    data.loc[len(data)]= [n_iter,malla ,valores_flujo[x1-1], valores_flujo[x2-1], valores_flujo[x3-1], runner1.converged]
    data.to_csv("EX1_data_modificado.csv", index=False)
    
if __name__ == "__main__":
    run()
    # data= pd.read_csv("EX1_data.csv")
    # data.to_excel("EX1_data.xlsx", index=False)
