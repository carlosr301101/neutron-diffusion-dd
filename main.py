



def main():
    NR= int(input("Ingrese el número de Regiones (NR): ")) # Numero de regiones
    NZ= int(input("Ingrese el número de Zonas (NZ): ")) # Numero de zonas materiales
    
    Izl= [int(input(f"Ingrese el tipo de material de la Zona {i+1}: ")) for i in range(NR)]
    SCT= [float(input(f"Ingrese la seccion de choque macroscopica total [cm^-1] {i+1}: ")) for i in range(NZ)]
    SCS= [float(input(f"Ingrese la seccion de choque macroscopica de dispersion [cm^-1] {i+1}: ")) for i in range(NZ)]
    
    Q_vec= [float(input(f"Ingrese la fuente volumetrica [n/cm^3-s] {i+1}: ")) for i in range(NR)]
    HR_vec= [float(input(f"Ingrese la espesura [cm] de la region {i+1}: ")) for i in range(NR)]
    
    N_cell= [int(input(f"Ingrese el número de celdas de la discretizacion espacial en la region {i+1}: ")) for i in range(NR)]
    
    N= int(input("Ingrese el número de  cuadratura de ángulos (Sn): ")) # Numero de angulos
    
    miu_i= [float(input(f"Ingrese el valor de mu para el angulo {i+1}: ")) for i in range(N)]
    wi= [float(input(f"Ingrese el peso asociado al angulo {i+1}: ")) for i in range(N)]

    epsilon= float(input("Ingrese la tolerancia para la convergencia del flujo: ")) # Tolerancia de convergencia
    
    # max_iter= int(input("Ingrese el número máximo de iteraciones: ")) # Maximo numero de iteraciones
    print(NR, NZ, Izl, SCT, SCS)
    
    

    print("Hello from curso-modelacion-flujo-n-clasico!")


if __name__ == "__main__":
    main()
