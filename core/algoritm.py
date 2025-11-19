import numpy as np
from .cuadraturas import DATA
import pandas as pd
import logging

logger= logging.getLogger(__name__)
# =================================================================
# Paso A: Datos de Entrada (Dados de entrada) [1, 2]
# =================================================================
class Config:
    logging.basicConfig(filename='Config.log',level=logging.INFO)
    def __init__(self, num_regions:int =0 , num_zones:int =0, epsilon:float =1e-5, max_iter:int =2000):
        self.num_regions = num_regions
        self.num_zones = num_zones
        if num_regions > 0 and num_zones > 0:
            logger.info("\n### Configurando el espacio de esas regiones:\n")
            self.space_config()
        elif num_zones > num_regions:
            raise ValueError("Número de zonas no puede ser mayor que el número de regiones.")
            
        else:
            logger.info("Número de regiones o zonas no válido.")
        logger.info("\n### Configurando las propiedades de los materiales:")
        self.materials_config()
        logger.info("### Configurando el orden de la cuadratura:\n")
        self.order_cuadrature()
        logger.info("### Realizando cálculos preliminares:\n")
        self.prelim_calculations()
          
    def space_config(self):
        self.NC = np.array([int(input(f"Introduzca la discretizacion espacial de la region: {i+1} -> ")) for i in range(self.num_regions)]) 
        self.HR = np.array([float(input(f"Introduzca el espesor en [cm] de la region: {i+1} -> ")) for i in range(self.num_regions)]) # Espesor de cada región (cm) [1, 2]
        self.IZL = np.array([int(input(f"Introduzca la ZONA de la region: {i+1} -> ")) for i in range(self.num_regions)])  # Mapeo de las zonas: 
             
    def materials_config(self):
        self.SCT = np.array([float(input(f"Introduzca Sección de choque macroscópica total de la ZONA: {i+1} -> ")) for i in range(self.num_zones)]) # Sección de choque macroscópica total (Sigma_T) [1, 2]
        self.SCS = np.array([float(input(f"Introduzca Sección de choque macroscópica de esparcimiento de la ZONA: {i+1} -> ")) for i in range(self.num_zones)]) # Sección de choque macroscópica de esparcimiento (Sigma_S) [1, 2]
        self.Q = np.array([float(input(f"Introduzca la Fuente de la ZONA: {i+1} -> ")) for i in range(self.num_regions)]) 
        
    def order_cuadrature(self):
        self.N = int(input("Introduzca el orden de cuadratura -> "))
        if self.N % 2 == 0:
            print(f"Orden de cuadratura S{self.N} seleccionado.")
        else: 
            raise ValueError("El orden de la cuadratura debe ser un número par.")         
        self.N_HALF = self.N // 2 # N/2 direcciones
        self.wights_directions()
    
    def wights_directions(self):
        dataframe= pd.DataFrame(DATA) 
        self.miu_m = dataframe.loc[(dataframe['N'] == self.N), 'mu_m'].values
        self.omega_m = dataframe.loc[(dataframe['N'] == self.N), 'omega_m'].values
        
    def prelim_calculations(self):
        # Cálculos preliminares
        self.NTC = np.sum(self.NC) # Total de celdas 
        self.NTP = self.NTC + 1 # Total de puntos 
        self.HC = np.array([hr/nc for hr, nc in zip(self.HR, self.NC)]) # Espesor de las celdas 
        
        
        
        
    
    def __str__(self) -> str:
        return f"\nConfiguracion del programa: {self.num_regions} regiones, {self.num_zones} zonas.\
            \nDiscretizacion espacial: {self.NC}\nEspesores: {self.HR}\nDistribucion de zonas: {self.IZL}\
            \nPropiedades materiales:\nSigma_T: {self.SCT}\nSigma_S: {self.SCS}\nFuentes: {self.Q}\
            \nOrden de cuadratura: S{self.N} con {self.N_HALF} direcciones.\
            \nPesos: {self.omega_m}\nDirecciones: {self.miu_m}\n"







# =================================================================
# Paso B: Cálculos Preliminares (Calcule) [1, 2]
# =================================================================
class Runner():
    def __init__(self, config:Config, reflexiva:bool=False):
        self.config = config
        self.converged:bool=False
        self.reflexiva=reflexiva
        
        self.S= np.zeros((config.NTC))  # Flujo angular inizializado en cero
        self.FORTH= np.zeros((config.NTP,config.N_HALF))  # Flujo angular hacia adelante
        self.BACK= np.zeros((config.NTP,config.N_HALF))  # Flujo angular hacia adelante
        logger.info(f"Runner inicializado correctamente con los siguientes datos\n{config}.\n")
        # logger.info(f"Matriz FORTH: {self.FORTH} , BACK: {self.BACK}")     
        if not reflexiva:
            self.boundary_conditions()
        else:
            self.boundary_reflexiva() 
    def boundary_conditions(self):
        self.FORTH[0]= [float(input(f"Ingrese el valor en la frontera IZQ de la cuadratura {i+1}")) for i in range(self.config.N_HALF)]
        self.BACK[0]= [float(input(f"Ingrese el valor en la frontera DER de la cuadratura {i+1}")) for i in range(self.config.N_HALF)]

    def boundary_reflexiva(self):
        self.FORTH[0]= np.ones(2)
        self.BACK[0]= np.ones(2)
    
    def __call__(self):
        
        def barre_izq():
            ### Iniciando barredura
            jf=1
            for jr in range(self.config.num_regions):
                iz= self.config.IZL[jr]
                xt= 0.5*self.config.SCT[iz]
                xc= self.config.HC[jr]
                f=self.config.Q[jr]
                gr=self.config.NC[jr]
                for j in range(gr):
                    jt=jf
                    jf=jf+1
                    esp= self.config.omega_m[jf]
                    
            pass
        def barre_derecha(self):
            pass
        
        pass
        

    
    def __str__(self) -> str:
        return f"Runner con configuración: {self.config}"


