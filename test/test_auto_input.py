"""Script de prueba para validar Config.auto_input con diccionario"""

import core.algoritm as alg

# Definir configuración como diccionario
config_dict = {
    "num_regions": 1,
    "num_zones": 1,
    "NC": [100],  # 100 celdas en región 1
    "HR": [100.0],  # Espesor de 100 cm
    "IZL": [1],  # Región 1 usa zona 1
    "SCT": [1.0],  # Sigma total = 1.0
    "SCS": [0.97],  # Sigma scattering = 0.97
    "Q": [1.0],  # Fuente = 1.0
    "N": 2,  # Orden S2
}

print("=" * 60)
print("PRUEBA: Config con auto_input desde diccionario")
print("=" * 60)

try:
    # Crear Config sin inputs manuales, pasando el diccionario como kwargs
    config = alg.Config(manual=False, reflexiva=True, **config_dict)

    print("\n✓ Configuración cargada exitosamente")
    print("\nPropiedades cargadas:")
    print(f"  - Regiones: {config.num_regions}")
    print(f"  - Zonas: {config.num_zones}")
    print(f"  - Celdas totales: {config.NTC}")
    print(f"  - Nodos: {config.NTP}")
    print(f"  - Cuadratura: S{config.N}")
    print(f"  - Direcciones: {config.N_HALF}")
    print(f"\n  - NC: {config.NC}")
    print(f"  - HR: {config.HR}")
    print(f"  - SCT: {config.SCT}")
    print(f"  - SCS: {config.SCS}")
    print(f"  - Q: {config.Q}")
    print(f"  - IZL: {config.IZL}")
    print(f"  - miu_m: {config.miu_m}")
    print(f"  - omega_m: {config.omega_m}")

    print("\n" + "=" * 60)
    print("Ahora probando Runner con reflexiva=True...")
    print("=" * 60)

    # Crear Runner con configuración cargada
    runner = alg.Runner(config)
    print("✓ Runner inicializado correctamente")

    # Ejecutar cálculo
    print("\nEjecutando barrido...\n")
    resultado = runner()

    print("\n✓ Cálculo completado")
    print(f"Iteraciones: {runner.iteration}")
    print(f"Convergido: {runner.converged}")
    print(f"Flujo escalar (primeras 10 celdas): {resultado[0][:10]}")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
