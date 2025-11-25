import core.algoritm as alg
import matplotlib.pyplot as plt
import numpy as np
# Parámetros del dominio y malla
NR = 1  # Número de regiones [1, 2]
NZ = 1  # Número de zonas de materiales [1, 2]

# Instanciar la clase Runner
config = alg.Config(NR, NZ)
runner1= alg.Runner(config)
valores_flujo= runner1()

x= np.arange(len(valores_flujo))
plt.plot(x, valores_flujo, marker='o')
plt.title("Flujo promedio a lo largo del dominio")
plt.xlabel("Índice de celda")
plt.ylabel("Flujo promedio")
plt.grid()
plt.show()
print(len(valores_flujo))
print("Valores obtenidos del flujo promedio:", valores_flujo)