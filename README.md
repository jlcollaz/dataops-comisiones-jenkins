# Proyecto DataOps: Comisiones con Docker y Jenkins

## 1. Opción elegida

Se eligió la opción A: Flujo DataOps con Docker y Jenkins.

Esta opción permite implementar un flujo de integración y despliegue continuo usando herramientas open source. El proceso automatiza la construcción de una imagen Docker, la ejecución del contenedor y la generación del archivo Excel de comisiones.

## 2. Estructura del proyecto

```text
dataops-comisiones-jenkins/
├── data/
│   └── ComisionEmpleados_V1_202605.csv
├── src/
│   └── calcular_comisiones.py
├── output/
│   └── .gitkeep
├── jenkins/
│   └── docker-compose.yml
├── docs/
│   └── diagrama-flujo.md
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── README.md
└── .gitignore
```

## 3. Ejecución local con Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/calcular_comisiones.py
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/calcular_comisiones.py
```

## 4. Ejecución local con Docker

```bash
docker build -t dataops-comisiones:latest .
docker run --rm -v "$(pwd)/output:/app/output" dataops-comisiones:latest
```

En Windows PowerShell:

```powershell
docker build -t dataops-comisiones:latest .
docker run --rm -v "${PWD}/output:/app/output" dataops-comisiones:latest
```

## 5. Ejecución con Jenkins

El archivo `Jenkinsfile` contiene las siguientes etapas:

1. Checkout del repositorio.
2. Construcción de la imagen Docker.
3. Ejecución automática del contenedor.
4. Validación del archivo Excel generado.
5. Archivado del artefacto generado.

## 6. Resultado esperado

El proceso genera el siguiente archivo:

```text
output/comisiones_calculadas.xlsx
```

Este archivo contiene tres hojas:

- `Detalle_Comisiones`: detalle de empleados y comisiones.
- `Resumen`: indicadores del proceso.
- `Control_DataOps`: evidencia de ejecución y trazabilidad.

## 7. Evidencias sugeridas para el informe final

- Repositorio GitHub con archivos versionados.
- Historial de commits.
- Captura del Dockerfile.
- Captura del Jenkinsfile.
- Captura del webhook configurado en GitHub.
- Captura del pipeline en Jenkins en estado exitoso.
- Captura del artefacto Excel generado.

Actualización para validar webhook automático desde GitHub hacia Jenkins.
