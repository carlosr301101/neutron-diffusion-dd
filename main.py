import core.algoritm as alg

# Parámetros del dominio y malla
NR = 2       # Número de regiones [1, 2]
NZ = 2       # Número de zonas de materiales [1, 2]

# Instanciar la clase Runner
runner = alg.Runner(NR, NZ)
print(runner)