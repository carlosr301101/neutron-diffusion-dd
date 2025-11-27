import core.algoritm as alg
from core.utils import calcular_desvios_relativos, func_analitica
from core.inputs import config_dict,config_dict_fino

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd    

def code_to_plot():
    config = alg.Config(num_regions=1,num_zones=1,manual=True,reflexiva=False)
    runner1 = alg.Runner(config)
    
    config_fino= alg.Config(manual=False, reflexiva=True, **config_dict_fino)
    runner_fino= alg.Runner(config_fino)
    
    resultado_fino = runner_fino() # Retorna diccionario
    valores_flujo_fino = resultado_fino['scalar_flux']
    
    resultado = runner1() # Retorna diccionario
    valores_flujo = resultado['scalar_flux']
    n_iter = resultado['iteration']
    
    # x_fino= np.arange(0,sum(config_fino.HR),0.5)
    
    malla = len(valores_flujo)
    h = sum(config.HR) / malla
    # Calcular coordenadas de las celdas (centros)
    x_celdas = np.arange(malla) * h + h/2
    valores_analiticos = np.array([func_analitica(x) for x in x_celdas]) # Flujo analitico para EX1
    
    
    # Calcular desvíos relativos
    step=1 # Cambiar el step para graficar la misma cantidad de datos de ambas mallas
    desvios_relativos = calcular_desvios_relativos(valores_flujo, valores_analiticos)
    
    # Crear figura con 2 subgráficas (lado a lado)
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    
    # Gráfica 1: Comparación de valores numéricos vs analíticos
    axes[0].plot(x_celdas, valores_analiticos, color='green', linewidth=2, label='Solución analítica')
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
    print("✓ Resultados guardados como: resultados_comparacion.xlsx")
    
    x1=int(10/h)
    x2=int(25/h)
    x3=int(40/h)

    data= pd.read_csv("EX1_data.csv")
    data.loc[len(data)]= [n_iter,malla ,valores_flujo[x1-1], valores_flujo[x2-1], valores_flujo[x3-1], resultado['converged']]
    data.to_csv("EX1_data_modificado.csv", index=False)
    
    
def run():
    config = alg.Config(manual=True,reflexiva=False)
    runner = alg.Runner(config)
    resultado = runner() # Retorna diccionario
    valores_flujo = resultado['scalar_flux']

    malla = len(valores_flujo)
    h = sum(config.HR) / malla
    # Calcular coordenadas de las celdas (centros)
    x_celdas = np.arange(malla) * h + h/2
    
    # Graficar
    plt.plot(x_celdas, valores_flujo, color='blue', label='Solución numérica')
    plt.xlabel('Posición x (cm)')
    plt.ylabel('Flujo escalar [n/m^2-s]')
    plt.savefig("Flujo.png", dpi=150)
    print("✓ Gráfica guardada como: Flujo.png")
    plt.show()
    
if __name__ == "__main__":
    # code_to_plot()
    # Estas lineas convierten la salida de csv a excel
    # data= pd.read_csv("EX1_data.csv")
    # data.to_excel("EX1_data.xlsx", index=False)
    run()