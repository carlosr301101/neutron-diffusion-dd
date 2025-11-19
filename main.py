import core.algoritm as alg

# Parámetros del dominio y malla
NR = 1  # Número de regiones [1, 2]
NZ = 1  # Número de zonas de materiales [1, 2]

# Instanciar la clase Runner
config = alg.Config(NR, NZ)
runner1= alg.Runner(config)
