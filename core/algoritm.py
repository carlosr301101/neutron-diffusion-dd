import numpy as np

# =================================================================
# Paso A: Datos de Entrada (Dados de entrada) [1, 2]
# =================================================================
class Runner:
    def __init__(self, num_regions:int =0 , num_zones:int =0, ):
        self.num_regions = num_regions
        self.num_zones = num_zones
        if num_regions > 0 and num_zones > 0:
            print("### Configurando el espacio de esas regiones:\n")
            self.space_config()
        elif num_zones > num_regions:
            raise ValueError("Número de zonas no puede ser mayor que el número de regiones.")
            
        else:
            print("Número de regiones o zonas no válido.")
        
        
    def space_config(self):
        self.NC = np.array([int(input(f"Introduzca la discretizacion espacial de la region: {i} -> ")) for i in range(self.num_regions)]) 
        self.HR = np.array([float(input(f"Introduzca el espesor en [cm] de la region: {i} -> ")) for i in range(self.num_zones)]) # Espesor de cada región (cm) [1, 2]
        
    def atoms_params(self):
        
        pass
    
    def __str__(self) -> str:
        return f"Configuracion del programa: {self.num_regions} regiones, {self.num_zones} zonas.\
            \nDiscretizacion espacial: {self.NC}\nEspesores: {self.HR}\n"



NC = np.array([100,200]) # Número de celdas de discretización espacial por región [1, 2]
HR = np.array([5,32]) # Espesor de cada región (cm) [1, 2]

# Propiedades del material (Se asume una única zona por simplicidad)
# Izquierda (Zona 1): sigma_t = 1.0, sigma_s = 0.99, Q = 2.0 (ejemplo genérico)
SCT = np.array([1.0,2]) # Sección de choque macroscópica total (Sigma_T) [1, 2]
SCS = np.array([0.99,0.98]) # Sección de choque macroscópica de esparcimiento (Sigma_S) [1, 2]
Q = np.array([2.0, 3]) # Fuente con intensidad constante (por región) [1, 2]
IZL = np.array([2,1]) # Mapeo de las zonas: Región 1 usa Zona 1 [1, 2]

# Parámetros angulares (Cuadratura S_N). Usaremos S2 como ejemplo (N=2)
N = 2        # Orden de la cuadratura angular S_N
N_HALF = N // 2 # N/2 direcciones [1, 2]

# Cuadratura Gauss-Legendre S2:
# mu_m > 0 (HI en la fuente) y pesos W [1, 2, 9]
HI = np.array([0.577350269189626]) # Ordenada discreta (mu_m) [1, 2, 9]
W = np.array([1.0]) # Peso de la cuadratura angular S_N [1, 2, 9]

# Criterio de convergencia [1, 2]
EPSILON = 1e-5 # Número de convergencia [1, 2]
MAX_ITER = 2000 # Límite de iteraciones