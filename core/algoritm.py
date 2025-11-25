import numpy as np
from .cuadraturas import DATA
import pandas as pd
import logging
from time import time

logger= logging.getLogger(__name__)
# =================================================================
# Paso A: Datos de Entrada (Dados de entrada) [1, 2]
# =================================================================
class Config:
    logging.basicConfig(filename='Config.log',level=logging.INFO)
    def __init__(self, num_regions:int =0 , num_zones:int =0, epsilon:float =1e-5, max_iter:int =2000):
        self.num_regions = num_regions
        self.num_zones = num_zones
        self.epsilon = epsilon
        self.max_iter = max_iter
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
        self.iteration:int=0
        
        self.S= np.zeros((config.NTC))  # Flujo angular inizializado en cero
        self.FORTH= np.zeros((config.NTP,config.N_HALF))  # Flujo angular hacia adelante
        self.BACK= np.zeros((config.NTP,config.N_HALF))  # Flujo angular hacia adelante
        self.average_flux= np.zeros((config.NTC))  # Flujo promedio en cada celda
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
        ## Aun no se ha terminado para que sea reflexiva, hay que modificar esta condicion.
    
    def barre_der(self):
            ### Iniciando barredura Izquierda
            start=time()
            logger.info("Iniciado Barrido a la Izquierda, e iniciando contador t")
            jf=0
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
                    for i in range(self.config.N_HALF):
                        od= self.config.omega_m[i]/xc
                        auxt= self.FORTH[jt][i]
                        num=(od-xt)*auxt+esp+f
                        den=od+xt
                        self.FORTH[jf][i]=num/den
            end=time()
            logger.info(f"Finalizado Barrido a la Derecha, y  finalizado contador t: {end-start} [s]")
                        
    def barre_izq(self):
            ### Iniciando barredura Derecha
            start=time()
            logger.info("Iniciado Barrido a la Derecha, e iniciando contador t")
            jf=self.config.NTP
            for jr in range(self.config.num_regions-1,-1,-1):
                iz= self.config.IZL[jr]
                xt= 0.5*self.config.SCT[iz]
                xc= self.config.HC[jr]
                f=self.config.Q[jr]
                gr=self.config.NC[jr]
                for j in range(gr):
                    jt=jf
                    jf=jf-1
                    esp= self.config.omega_m[jf]
                    for i in range(self.config.N_HALF):
                        od= self.config.omega_m[i]/xc
                        auxt= self.FORTH[jt][i]
                        num=(od-xt)*auxt+esp+f
                        den=od+xt
                        self.BACK[jf][i]=num/den
            end=time()
            logger.info(f"Finalizado Barrido a la Derecha, y finalizado contador t: {end-start} [s]")
            
    def calculo_flujo(self):
            start=time()
            logger.info("Iniciado Cálculo de flujo, e iniciando contador t")
            for j in range(self.config.NTC):
                jf=j+1
                suma=0.0
                
                for id in range(self.config.N_HALF):
                    aux1= 0.5*(self.FORTH[jf][id]+ self.FORTH[j][id])
                    aux2= 0.5*(self.BACK[jf][id]+ self.BACK[j][id])
                    peso= self.config.omega_m[id]
                    suma= suma + peso*(aux1 + aux2)
                    self.S[j]= self.S[j]+ self.config.omega_m[id]*(self.FORTH[j][id]+ self.BACK[j+1][id])
                
                self.average_flux[j]= suma
                
            end=time()
            logger.info(f"Finalizado Cálculo de flujo, y finalizado contador t: {end-start} [s]")

    def actuializa_fuente(self):
            start=time()
            js=0
            logger.info("Iniciado Actualización de fuente, e iniciando contador t")
            
            for jr in range(self.config.num_regions):
                iz= self.config.IZL[jr]
                xs= 0.5*self.config.SCS[iz]
                gr=self.config.NC[jr]
                for jc in range(gr):
                    js=js+1
                    self.S[js]= xs*self.average_flux[js]

            end=time()
            logger.info(f"Finalizado Actualización de fuente, y finalizado contador t: {end-start} [s]")

    def check_convergence(self,old_flux, new_flux):
            relative_change = np.abs((new_flux - old_flux) / (new_flux + 1e-10))  # Evitar división por cero
            max_change = np.max(relative_change)
            logger.info(f"Cambio máximo relativo en el flujo: {max_change}")
            return max_change <= self.config.epsilon
        
    def check_max_iterations(self):
            if self.iteration >= self.config.max_iter:
                print("Se ha alcanzado el número máximo de iteraciones sin convergencia.")
                logger.warning("Se ha alcanzado el número máximo de iteraciones sin convergencia.")
                return True
            return False
# =================================================================
# Paso C: Cálculos segun la metodologia a seguir
# =================================================================
    def __call__(self):
        while not self.converged:
            old_flux= self.average_flux.copy()
            self.iteration += 1
            logger.info(f"Iniciando Iteración número: {self.iteration}")
            self.barre_der()
            self.barre_izq()
            self.calculo_flujo()
            self.actuializa_fuente()
            self.converged= self.check_convergence(old_flux, self.average_flux)
            if self.check_max_iterations():
                break
        
        return self.average_flux
    
        


        
        
        
    
    def __str__(self) -> str:
        return f"Runner con configuración: {self.config}"


