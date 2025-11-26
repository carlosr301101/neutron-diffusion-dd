import core.algoritm as alg
import matplotlib.pyplot as plt
import numpy as np
from math import exp
import pandas as pd
# Parámetros del dominio y malla
NR = 1  # Número de regiones [1, 2]
NZ = 1  # Número de zonas de materiales [1, 2]

# Instanciar la clase Runner
def func_analitica(x):
    return 1.705*exp(-0.3*x)

def run():
    config = alg.Config(manual=True)
    runner1= alg.Runner(config)
    valores_flujo, n_iter= runner1()

    malla= len(valores_flujo)
    h=100//malla



    x_line= np.linspace(0, len(valores_flujo),malla)
    y= np.array([func_analitica(i) for i in x_line])

    points = np.column_stack((x_line, valores_flujo))


    ## Parte de graficar los valores como puntos los numericos y la funcion analitica
    # plt.scatter(points[:, 0], points[:, 1], color='blue', label='Valores numericos')
    # plt.plot(x_line, y, color="green" ,label='Valores analiticos')
    # plt.title("Flujo promedio a lo largo del dominio")
    # plt.xlabel(f"Índice de celda, malla x:[{malla}]")
    # plt.ylabel("Flujo promedio")

    # plt.grid()
    # plt.legend()
    # plt.savefig("salva.png")
    
    
    # Con esto aseguramos que se analicen los puntos x1, x2, x3 para -> 10, 20, 50
    x1=10//h
    x2=20//h
    x3=50//h
    data= pd.read_csv("EX1_data.csv")
    data.loc[len(data)]= [n_iter,malla ,valores_flujo[x1-1], valores_flujo[x2-1], valores_flujo[x3-1], runner1.converged]
    
    data.to_csv("EX1_data_modificado.csv", index=False)

run()

