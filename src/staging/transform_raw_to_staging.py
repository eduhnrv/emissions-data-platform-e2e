"""
transform_raw_to_staging.py
===========================

Transformo archivos RAW (2005–2026) de emisiones a cuerpos de agua a un dataset
STAGING unificado bajo el esquema canónico v1 (consultar en /docs/schema_mapping.md).

- Respeta RAW (no modifica archivos originales).
- Normalizo nombres, encoding y tipos.
- Agrego metadatos de trazabilidad: source_file y fecha_ingestion.
- Exporto a Parquet para consumo analítico.

Proyecto: Environmental Data Platform – End-to-End Emissions Analytics
Autor : Eduardo S. Henriquez N.
Fecha : 19 / 01 / 26.
"""
# Diferir evaluación de anotaciones de tipo para mejorar rendimiento y compatibilidad
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List

import pandas as pd

#===================
#Definición de Rutas
#===================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
STAGING_DIR = PROJECT_ROOT / "data" / "staging"
OUT_FILE = STAGING_DIR / "emisiones_staging.parquet"

#===================
#Esquema canónico v1
#===================

CANONICAL_COLUMNS: List[str] = [
    #metadatos
    "source_file",
    "fecha_ingestion",
    #tiempo
    "anio",
    #establecimiento
    "razon_social",
    "rut_razon_social",
    "nombre_establecimiento",
    "id_vu",
    #clasificación económica
    "ciiu4",
    "ciiu4_id",
    "ciiu6",
    "ciiu6_id",
    "rubro",
    "rubro_id",
    #geografía
    "region",
    "provincia",
    "comuna",
    "codigo_territorial",
    #ubicación
    "latitud",
    "longitud",
    # infraestructura
    "ducto",
    "nombre_ducto",
    #emision y campo técnico
    "contaminante",
    "contaminante_id",
    "emision_toneladas",
    "norma",
    "tabla",
    "origen",
]

#==================
#Mapeo por período
#==================

#2005-2007: headers con espacios, acentos, separador ";"
RENAME_2005_2017: Dict[str, str] = {
    "Razón social": "razon_social",
    "Nombre de establecimiento": "nombre_establecimiento",
    "ID establecimiento (VU)": "id_vu",
    "CIIU4": "ciiu4",
    "Rubro RETC": "rubro",
    "Ducto": "ducto",
    "Tipo de Contaminante": "contaminante",
    "Emisión (toneladas)": "emision_toneladas",
    "Año": "anio",
    "Norma": "norma",
    "Región": "region",
    "Provincia": "provincia",
    "Comuna": "comuna",
    #legacy no se mapea a lat/long en v1:
    #"Huso", "Coordenada norte", "Coordenada este".

}


# 2018–2023: separador ';' y encoding irregular (a�o)
RENAME_2018_2023: Dict[str, str] = {
    "año": "anio",
    "a�o": "anio",
    "razon_social": "razon_social",
    "rut_razon_social": "rut_razon_social",
    "nombre_establecimiento": "nombre_establecimiento",
    "id_vu": "id_vu",
    "ciiu4": "ciiu4",
    "id_ciiu4": "ciiu4_id",
    "ciiu6": "ciiu6",
    "id_ciiu6": "ciiu6_id",
    "rubro_vu": "rubro",
    "id_rubro_vu": "rubro_id",
    "region": "region",
    "provincia": "provincia",
    "comuna": "comuna",
    "comuna_": "comuna",
    "id_comuna": "codigo_territorial",
    "latitud": "latitud",
    "longitud": "longitud",
    "cantidad_toneladas": "emision_toneladas",
    "contaminantes": "contaminante",
    "id_contaminantes": "contaminante_id",
    "id_contaminantes ": "contaminante_id",  #header id_contaminantes vienen con espacio
    "ducto": "ducto",
    "norma": "norma",
    "nombre_ducto": "nombre_ducto",
    "tabla": "tabla",
    "origen": "origen",
}

# 2024–2026: CSV con "," limpio
RENAME_2024_2026: Dict[str, str] = {
    "año": "anio",
    "id_vu": "id_vu",
    "razon_social": "razon_social",
    "rut_razon_social": "rut_razon_social",
    "nombre_establecimiento": "nombre_establecimiento",
    "ciiu4": "ciiu4",
    "ciiu4_id": "ciiu4_id",
    "ciiu6": "ciiu6",
    "ciiu6_id": "ciiu6_id",
    "rubro": "rubro",
    "rubro_id": "rubro_id",
    "region": "region",
    "provincia": "provincia",
    "comuna": "comuna",
    "codigo_unico_territorial": "codigo_territorial",
    "latitud": "latitud",
    "longitud": "longitud",
    "ducto": "ducto",
    "ducto_nombre": "nombre_ducto",
    "contaminante": "contaminante",
    "contaminante_id": "contaminante_id",
    "emision_total": "emision_toneladas",
    "norma": "norma",
    "tabla": "tabla",
    "origen": "origen",
}

@dataclass(frozen=True)
class RawFileSpec:
    path: Path
    sep: str
    encoding: str
    rename_map: Dict[str, str]

def _read_raw(spec: RawFileSpec) -> pd.DataFrame:
    """
    Lee Raw según separador/encoding y normaliza headers básicos.
    """
    df = pd.read_csv(spec.path, sep=spec.sep, encoding=spec.encoding, dtype=str)
    #normalizo headers: strip espacios
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns=spec.rename_map)
    return df

def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Casteos a tipo lógico conforme a esquema canónico v1.
    """
    #anio --> Int64(nullable)
    if "anio" in df.columns:
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype("Int64")
    
    #emision_toneladas -> Float
    if "emision_toneladas" in df.columns:
        s = df["emision_toneladas"].astype(str).str.replace(",", ".", regex=False)
        df["emision_toneladas"] = pd.to_numeric(s, errors="coerce")

    # lat/long -> float
    for col in ["latitud", "longitud"]:
        if col in df.columns:
            s = df[col].astype(str).str.replace(",", ".", regex=False)
            df[col] = pd.to_numeric(s, errors="coerce")

    # IDs -> string (pandas string dtype)
    id_cols = ["id_vu", "rut_razon_social", "ciiu4_id", "ciiu6_id", "rubro_id", "contaminante_id", "codigo_territorial"]
    for col in id_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # strings generales: strip
    for col in df.columns:
        if df[col].dtype == object or str(df[col].dtype) == "string":
            df[col] = df[col].astype("string").str.strip()

    return df


def _ensure_canonical(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aseguro todas las columnas canónicas presentes y en orden.
    """
    for col in CANONICAL_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df[CANONICAL_COLUMNS]


def build_staging() -> Path:
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    specs: List[RawFileSpec] = [
        RawFileSpec(RAW_DIR / "2005-2017.csv", sep=";", encoding="utf-8", rename_map=RENAME_2005_2017),
        RawFileSpec(RAW_DIR / "2018.csv", sep=";", encoding="latin-1", rename_map=RENAME_2018_2023),
        RawFileSpec(RAW_DIR / "2019.csv", sep=";", encoding="latin-1", rename_map=RENAME_2018_2023),
        RawFileSpec(RAW_DIR / "2020.csv", sep=";", encoding="latin-1", rename_map=RENAME_2018_2023),
        RawFileSpec(RAW_DIR / "2021.csv", sep=";", encoding="latin-1", rename_map=RENAME_2018_2023),
        RawFileSpec(RAW_DIR / "2022.csv", sep=";", encoding="latin-1", rename_map=RENAME_2018_2023),
        RawFileSpec(RAW_DIR / "2023.csv", sep=";", encoding="latin-1", rename_map=RENAME_2018_2023),
        RawFileSpec(RAW_DIR / "2024-2026.csv", sep=",", encoding="utf-8", rename_map=RENAME_2024_2026),
    ]

    frames: List[pd.DataFrame] = []
    ingest_date = date.today().isoformat()

    for spec in specs:
        df = _read_raw(spec)

        # metadatos
        df["source_file"] = spec.path.name
        df["fecha_ingestion"] = ingest_date

        df = _coerce_types(df)
        df = _ensure_canonical(df)
        frames.append(df)

    staging = pd.concat(frames, ignore_index=True)

    # export
    staging.to_parquet(OUT_FILE, index=False)
    return OUT_FILE


if __name__ == "__main__":
    out = build_staging()
    print(f"STAGING generado: {out}")

