# Modelación de flujo n-clásico (Diamond Difference)

## ⚛️ Simulador de Transporte de Neutrones 1D (Diamond Difference - $S_N$)

## 📝 Descripción del Proyecto

Este repositorio contiene una implementación en Python de un solver unidimensional de transporte neutral de partículas usando la metodología Diamond Difference (DD) con iteración de fuente. Está pensado para estudios numéricos, validación contra soluciones analíticas y experimentos de sensibilidad.

**Resumen rápido**
- Implementa cuadratura S_N (p. ej. S2) y barridos angulares para resolver la ecuación de transporte unidimensional.
- Usa el esquema Diamond Difference para el barrido y realiza correcciones tipo "step-difference" (fixup) si el esquema produce resultados no físicos.
- Permite entradas interactivas y carga de configuración desde diccionarios (modo `auto_input`) para ejecución no interactiva.

**Lenguaje:** Python 3.13+

## **Archivos principales**
- `main.py` : Script de ejemplo para ejecutar simulaciones y generar gráficas comparativas.
- `core/algoritm.py` : Implementación principal — clases `Config` y `Runner`.
  - `Config`: gestión de entradas (manual o por diccionario), cálculo preliminar de vectores de propiedades por celda.
  - `Runner`: barridos (sweep), cálculo de flujo escalar, chequeo de convergencia y condición reflexiva opcional.
- `core/cuadraturas.py` : Tabla/constantes de órdenes de cuadratura (S_N) — pesos y cosenos.
- `core/input.py` : En este fichero se configura el diccionario con los valores de entrada cuando se activa el modo automatico de entrada

**Modulos de python necesarios para ejecurtar**
dependencies = [
    "matplotlib>=3.10.7",
    "numpy>=2.3.5",
    "openpyxl>=3.1.5",
    "pandas>=2.3.3",
]

*Recomiendo el uso de un gestor de paquetes, especificamente `UV`([link](https://docs.astral.sh/uv)) para manejar el entorno virtual y tener organizado el proyecto, en dicho caso se ejecutaria el programa haciendo en consola*
`uv sync` -> Para cargar los modulos necesarios
`uv run main.py` -> Ejecutar el programa sin ningun tipo de problema de versiones de python o modulos.

**Ideas/archivos extra**
- `resultados_comparacion.csv/xlsx` : archivos generados con resultados numéricos y desviaciones.
- `comparacion_flujos.png` : figura comparativa (analítico vs numérico) generada por `main.py`.

## **Conceptos principales del algoritmo**

1. Ecuación de transporte 1D (línea integral):

   μ dψ/dx + Σ_t ψ = 1/2 Σ_s φ + Q

   - ψ(x, μ): flujo angular
   - φ(x) = ∑_m w_m ψ_m(x): flujo escalar
   - Σ_t, Σ_s: secciones macroscópicas
   - Q: fuente externa

2. Diamond Difference (DD) por celda (celdas i con espesor Δx):

   ψ_out = [ (μ/Δx - Σ_t/2) ψ_in + S ] / (μ/Δx + Σ_t/2)

   - ψ_in: valor en el nodo de entrada de la celda
   - ψ_out: valor en el nodo de salida
   - S: fuente total en la celda (a menudo 0.5*(Q + Σ_s φ) si hay scattering isotrópico)

3. Corrección (Fixup): si DD produce ψ_out negativo, se aplica un esquema Step Difference (SD) para mantener no negatividad.

4. Fuente iterativa (Source Iteration):
   - Se calcula la fuente total usando el φ antiguo, se realiza un sweep (derecha e izquierda), se actualiza φ y se repite hasta convergencia.

## **Convenciones y unidades**
- Longitud en centímetros (cm) por defecto.
- Se asume discretización por regiones; cada región tiene `NC[r]` celdas y espesor `HR[r]`.
- `IZL` mapea cada región a una zona de material (valores 1-based).

## **Uso — modo interactivo**

1) Ejecutar el script principal y seguir los inputs:

`python main.py`

El programa pedirá:
- número de regiones y zonas (si no se pasan por `Config`),
- `NC`, `HR`, `IZL`, propiedades de material (`SCT`, `SCS`, `Q`),
- orden de cuadratura `N` (p. ej. 2) y condiciones de frontera (valores incidentes).

Al finalizar crea la figura `comparacion_flujos.png` y el fichero `resultados_comparacion.xlsx`.

**Uso — modo automático (desde diccionario)**

Puedes cargar toda la configuración desde un diccionario (ideal para scripts batch). Ejemplo mínimo:

```python
from core.algoritm import Config, Runner

cfg = {
  'num_regions': 1,
  'num_zones': 1,
  'NC': [100],
  'HR': [100.0],
  'IZL': [1],
  'SCT': [1.0],
  'SCS': [0.97],
  'Q': [1.0],
  'N': 2
}

config = Config(manual=False, reflexiva=True, **cfg)
runner = Runner(config)
phi, n_iter, psi_right, psi_left = runner()
```

`Config.auto_input` valida dimensiones y tipos, construye vectores por celda (`sigma_t_vec`, `dx_vec`, etc.) y llama a `prelim_calculations()`.

**Salida de `Runner`**
- `scalar_flux` (φ por celda) — array de tamaño `NTC`.
- `iteration` — número de iteraciones realizadas.
- `PSI_RIGHT` y `PSI_LEFT` — matrices nodales de flujos angulares (tamaños `NTP x N_HALF`).

**Ejemplos incluidos**
- `test_auto_input.py`: prueba automatizada que carga un diccionario y ejecuta `Runner`.
- `ejemplo_auto_input.py`: ejemplos y documentación de uso.


**Problemas comunes y soluciones**
- IndexError al acceder a zonas: verificar que `IZL` es 1-based y valores ≤ `num_zones`.
- Valores constantes en primeras celdas: comprobar condiciones de frontera (BACK debe colocarse en nodo derecho `NTP-1`).
- Convergencia lenta: reducir `epsilon` o usar acceleración (no implementada actualmente).

<!-- **Tests y ejecución rápida**
1) Test de auto-configuración:

```powershell
python test_auto_input.py
```

2) Ejecutar ejemplo comparativo y guardar resultados:

```powershell
python main.py
```

3) Ejecutar el ejemplo de demostración (no interactivo):

```powershell
python ejemplo_auto_input.py
``` -->
-------

## **Estructura del proyecto**

```
.
├─ main.py
├─ pyproject.toml
├─ core/
│  ├─ __init__.py
  │  ├─ algoritm.py   # Config, Runner, sweep, DD
  │  └─ cuadraturas.py
└─ doc/
```

