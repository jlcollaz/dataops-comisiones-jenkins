"""
Proceso DataOps: cálculo y generación de reporte de comisiones.

Este script lee un archivo CSV de comisiones, realiza validaciones básicas,
calcula indicadores de control y genera un archivo Excel como artefacto final.

Entrada esperada:
- data/ComisionEmpleados_V1_202605.csv

Salida esperada:
- output/comisiones_calculadas.xlsx
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = Path(os.getenv("INPUT_FILE", BASE_DIR / "data" / "ComisionEmpleados_V1_202605.csv"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "output"))
OUTPUT_FILE = OUTPUT_DIR / "comisiones_calculadas.xlsx"


def leer_datos(path: Path) -> pd.DataFrame:
    """Lee el archivo CSV usando separador punto y coma."""
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {path}")

    df = pd.read_csv(path, sep=";", encoding="utf-8")
    df.columns = [col.strip() for col in df.columns]
    return df


def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia, valida y prepara el detalle de comisiones."""
    columnas_requeridas = {"empleado_id", "Nombre y Apellido", "Comisión"}
    faltantes = columnas_requeridas - set(df.columns)

    if faltantes:
        raise ValueError(f"Faltan columnas requeridas en el CSV: {sorted(faltantes)}")

    detalle = df.copy()
    detalle["empleado_id"] = pd.to_numeric(detalle["empleado_id"], errors="coerce").astype("Int64")
    detalle["Comisión"] = pd.to_numeric(detalle["Comisión"], errors="coerce")
    detalle["Nombre y Apellido"] = detalle["Nombre y Apellido"].astype(str).str.strip()

    # Separación referencial del campo 'Nombre y Apellido'.
    partes = detalle["Nombre y Apellido"].str.split(",", n=1, expand=True)
    detalle["nombre"] = partes[0].str.strip()
    detalle["apellido"] = partes[1].str.strip() if partes.shape[1] > 1 else ""

    detalle = detalle.rename(columns={"Comisión": "comision_bruta"})

    # Cálculo simple y trazable para el artefacto final.
    # La comisión neta se mantiene igual porque no se proporcionó una regla de descuento adicional.
    detalle["comision_neta"] = detalle["comision_bruta"]
    detalle["estado_validacion"] = "OK"

    detalle.loc[detalle["empleado_id"].isna(), "estado_validacion"] = "ERROR: empleado_id vacío o inválido"
    detalle.loc[detalle["comision_bruta"].isna(), "estado_validacion"] = "ERROR: comisión vacía o inválida"
    detalle.loc[detalle["comision_bruta"] < 0, "estado_validacion"] = "ERROR: comisión negativa"

    detalle = detalle[
        [
            "empleado_id",
            "Nombre y Apellido",
            "nombre",
            "apellido",
            "comision_bruta",
            "comision_neta",
            "estado_validacion",
        ]
    ]

    return detalle


def construir_resumen(detalle: pd.DataFrame) -> pd.DataFrame:
    """Construye un resumen ejecutivo del proceso."""
    total_registros = len(detalle)
    registros_ok = int((detalle["estado_validacion"] == "OK").sum())
    registros_error = total_registros - registros_ok

    resumen = pd.DataFrame(
        [
            ["Total de registros procesados", total_registros],
            ["Registros correctos", registros_ok],
            ["Registros con observación", registros_error],
            ["Monto total de comisión bruta", detalle["comision_bruta"].sum()],
            ["Monto total de comisión neta", detalle["comision_neta"].sum()],
            ["Comisión promedio", detalle["comision_neta"].mean()],
            ["Comisión mínima", detalle["comision_neta"].min()],
            ["Comisión máxima", detalle["comision_neta"].max()],
        ],
        columns=["Indicador", "Valor"],
    )
    return resumen


def construir_control() -> pd.DataFrame:
    """Genera una hoja de control para evidenciar reproducibilidad DataOps."""
    return pd.DataFrame(
        [
            ["Proceso", "Cálculo de comisiones"],
            ["Herramienta", "Python + Docker + Jenkins"],
            ["Archivo de entrada", str(INPUT_FILE)],
            ["Archivo de salida", str(OUTPUT_FILE)],
            ["Fecha de ejecución", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ],
        columns=["Campo", "Detalle"],
    )


def generar_excel(detalle: pd.DataFrame, resumen: pd.DataFrame, control: pd.DataFrame) -> None:
    """Genera el archivo Excel final."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        detalle.to_excel(writer, sheet_name="Detalle_Comisiones", index=False)
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
        control.to_excel(writer, sheet_name="Control_DataOps", index=False)

        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            for column_cells in ws.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 45)


def main() -> None:
    print("Iniciando proceso DataOps de cálculo de comisiones...")
    print(f"Archivo de entrada: {INPUT_FILE}")

    df = leer_datos(INPUT_FILE)
    detalle = transformar_datos(df)
    resumen = construir_resumen(detalle)
    control = construir_control()
    generar_excel(detalle, resumen, control)

    print(f"Registros procesados: {len(detalle)}")
    print(f"Archivo generado correctamente: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
