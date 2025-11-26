import core.algoritm as alg
import matplotlib.pyplot as plt
import numpy as np
from math import exp
# Parámetros del dominio y malla
NR = 1  # Número de regiones [1, 2]
NZ = 1  # Número de zonas de materiales [1, 2]

# Instanciar la clase Runner
config = alg.Config(manual=False,NC=2)
runner1= alg.Runner(config)
valores_flujo= runner1()

def func_analitica(x):
    return 1.705*exp(-0.3*x)

x_line= np.linspace(0, len(valores_flujo),len(valores_flujo))
print(x_line)

y= np.array([func_analitica(i) for i in x_line])
print(y)
points = np.column_stack((x_line, valores_flujo))


## Parte de graficar los valores como puntos los numericos y la funcion analitica
plt.scatter(points[:, 0], points[:, 1], color='blue', label='Valores numericos')
plt.plot(x_line, y, color="green" ,label='Valores analiticos')
plt.title("Flujo promedio a lo largo del dominio")
plt.xlabel("Índice de celda")
plt.ylabel("Flujo promedio")

plt.grid()
plt.legend()
plt.savefig("salva.png")
plt.show()
print(len(valores_flujo))
print("Valores obtenidos del flujo promedio:", valores_flujo)