"""
insights.py
===========

Genera insights y reporte (tablas y figuras) a partir de dataset.
Staging : data/staging/emisiones_staging.parquet

Outputs:
- reports/tables/*.csv
- reports/figures/*.png

Autor: Eduardo S. Henríquez N.
Proyecto: Environmental Data Platform - End-to-End Emissions Analytics
Fecha: 20 / 01 / 26. 
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

#==============
#Paths / config
#==============

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STAGING_FILE = PROJECT_ROOT / "data" / "staging" / "emisiones_staging.parquet"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLE_DIR = REPORTS_DIR / "tables"

def ensure_dirs() -> None:
    """
    Crea (si no existen) los directorios de salida para reportes.
    
    Directorios:
    ------------
        -reports/figures
        -reports/tables
    
    Returns:
    --------
    None.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    
def load_staging() -> pd.DataFrame:
    """
    Carga el dataset staging desde parquet.

    Returns:
    --------
    pandas.DataFrame
        DataFrame con el esquema canónico v1.

    Raises:
    -------
    FileNotFoundError
        Si el archivo parquet staging no existe en la ruta correspondiente.

    """
    if not STAGING_FILE.exists():
        raise FileNotFoundError(f"No se encontró archivo Parquet Staging en : {STAGING_FILE}")
    return pd.read_parquet(STAGING_FILE)

def save_table(df: pd.DataFrame, name: str) -> Path:
    """
    Persistencia de una tabla (DataFrame) como csv en reports/tables.

    Parameters:
    -----------
    df: pandas.DataFrame
        Tabla a persistir.
    name: str 
        Nombre base del archivo (sin extensión)

    Returns:
    --------
    pathlib.Path
        Ruta del archivo generado

    Note:
    -----
    - Escribe un archivo csv en reports/tables/{name}.csv
    """

    out = TABLE_DIR / f"{name}.csv"
    df.to_csv(out, index=False)
    return out

def save_fig(path: Path) -> None:
    """
    Guarda la figura activa de Matplotlib en disco y libera recursos

    Parameters:
    -----------
    path: pathlib.Path
        Ruta del archivo de salida (ej: reports/figures/fig.png)

    Return:
    -------
    None.

    Notes:
    ------
        -Evita uso de memoria indebido usando 'plt.close()'
        -Se utiliza 'tight_layout()' para mejorar el espaciado automático
    """
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


#=============
#Insights
#=============

def emissions_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula emisiones totales por año y genera tabla y figura de salida.
        -Tabla : reports/tables/emisiones_por_anio.csv
        -Figura: reports/figures/emisiones_por_anio.png

    Parameters:
    -----------
    df: pandas.DataFrame
        Dataset staging con columnas:
            -anio
            -emision_toneladas
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame con columnas:
            -anio
            -emision_total_ton
    """
    g = (
        df.groupby("anio", dropna=True)["emision_toneladas"]
        .sum(min_count=1)
        .reset_index(name="emision_total_ton")
        .sort_values("anio")
    )
    
    save_table(g, "emisiones_por_anio")

    plt.figure()
    plt.plot(g["anio"], g["emision_total_ton"])
    plt.title("Emisiones totales por año")
    plt.xlabel("Año")
    plt.ylabel("Emision total(toneladas)")
    save_fig(FIGURES_DIR / "emisiones_por_anio.png")

    return g

def top_regions(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Obtiene el Top N de regiones por emisiones acumuladas y genera salidas.
        -Tabla: reports/tables/top_regiones.csv
        -Figura: reports/figures/top_regiones.png

    Parameters:
    -----------
    df: pd.DataFrame
        Dataset staging con columnas:
            -region
            -emision_toneladas
    top_n: int, default = 10
        Número de regiones a incluir en el ranking

    Returns:
    --------
    pandas.DataFrame
        DataFrame con columnas:
            -region
            -emision_total_ton
    
    """
    g = (
        df.groupby("region", dropna=True)["emision_toneladas"]
        .sum(min_count=1)
        .reset_index(name="emision_total_ton")
        .sort_values("emision_total_ton", ascending=False)
        .head(top_n)
    )
    save_table(g, "top_regiones")

    plt.figure()
    plt.bar(g["region"].astype(str), g["emision_total_ton"])
    plt.title(f"Top {top_n} regiones por emisiones (acumulado)")
    plt.xlabel("Región")
    plt.ylabel("Emisión total (toneladas)")
    plt.xticks(rotation=45, ha="right")
    save_fig(FIGURES_DIR / "top_regiones.png")

    return g

def top_contaminants(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Obtiene el top_n de contaminantes por emisiones acumuladas y genera salidas.
        -Tabla: reports/tables/top_contaminantes.csv
        -Figura: reports/figures/top_contaminantes.png

    Parameters:
    -----------
    df: pandas.DataFrame
        Dataset staging con columnas:
            -contaminante
            -emision_toneladas
    top_n: int, default = 10
        Número de contaminantes a incluir en el ranking.

    Returns:
    --------
    pandas.DataFrame
        DataFrame con columnas:
            -contaminante
            -emision_total_ton
    """
    g = (
        df.groupby("contaminante", dropna=True)["emision_toneladas"]
        .sum(min_count=1)
        .reset_index(name="emision_total_ton")
        .sort_values("emision_total_ton", ascending=False)
        .head(top_n)
    )
    save_table(g, "top_contaminantes")

    plt.figure()
    plt.bar(g["contaminante"].astype(str), g["emision_total_ton"])
    plt.title(f"Top {top_n} contaminantes por emisiones(acumulado)")
    plt.xlabel("Contaminante")
    plt.ylabel("Emision total (toneladas)")
    plt.xticks(rotation=45, ha="right")
    save_fig(FIGURES_DIR / "top_contaminantes.png")
    
    return g

def top_emitters_concentration(df: pd.DataFrame, top_pct: float = 0.05) -> pd.DataFrame:
    """
    Estima concentración de emisiones por emisor (establecimiento) y guarda resultado.

    Se calcula el aporte del Top X% (por defecto 5%) de emisores sobre el total
    de emisiones. El agrupador principal es id_vu; si no existe, se usa
    razon_social como fallback.

        - Tabla: reports/tables/concentracion_top_emisores.csv

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset staging con columnas al menos:
            - emision_toneladas
        y preferentemente:
            - id_vu (si no existe, se usa razon_social)
    top_pct : float, default=0.05
        Porcentaje superior de emisores a considerar (0 < top_pct <= 1).

    Returns
    -------
    pandas.DataFrame
        DataFrame con métricas agregadas:
        - group_key
        - emitters_total
        - top_pct
        - top_n
        - emision_total_ton
        - emision_top_ton
        - share_top

    Notes
    -----
    - Si el total de emisiones es 0, share_top se reporta como 0.0.
    - Esta métrica es útil para evidenciar concentración (pareto) en el dominio.
    """
    if not (0 < top_pct <= 1):
        raise ValueError("top_pct debe estar en el rango (0, 1].")

    #Se mide concentración por establecimiento(id_vu). si faltara -> razón_social
    key = "id_vu" if "id_vu" in df.columns else "razon_social"

    s = (
        df.groupby(key, dropna=True)["emision_toneladas"]
        .sum(min_count=1)
        .dropna()
        .sort_values(ascending=False)
    )

    total = float(s.sum())
    n_emitters = int(len(s))
    top_n = max(1, int(n_emitters * top_pct))
    top_sum = float(s.head(top_n).sum())
    share = (top_sum / total) if total > 0 else 0.0

    out = pd.DataFrame(
        [{
            "group_key": key,
            "emitters_total": n_emitters,
            "top_pct": top_pct,
            "top_n": top_n,
            "emision_total_ton": total,
            "emision_top_ton": top_sum,
            "share_top": share,
        }]
    )

    save_table(out, "concentracion_top_emisores")
    return out


def main() -> None:
    """
    Punto de entrada (CLI) para ejecutar todos los insights y generar outputs.

    Flujo
    -----
    1) Crea directorios de reportes.
    2) Carga dataset STAGING desde Parquet.
    3) Ejecuta:
        - emisiones por año
        - top regiones
        - top contaminantes
        - concentración top emisores
    4) Imprime un resumen breve en consola para trazabilidad.

    Returns
    -------
    None
    """
    ensure_dirs()
    df = load_staging()

    print("=== Analytics: Insights (STAGING) ===")
    print(f"Input: {STAGING_FILE}")
    print(f"Shape: {df.shape}")

    r1 = emissions_by_year(df)
    r2 = top_regions(df, top_n=10)
    r3 = top_contaminants(df, top_n=10)
    r4 = top_emitters_concentration(df, top_pct=0.05)

    print("\n=== Outputs ===")
    print(f"- Figures: {FIGURES_DIR}")
    print(f"- Tables : {TABLE_DIR}")

    # Resumen corto (para terminal)
    anio_min = int(r1["anio"].min()) if len(r1) and pd.notna(r1["anio"].min()) else None
    anio_max = int(r1["anio"].max()) if len(r1) and pd.notna(r1["anio"].max()) else None

    top_region = str(r2.iloc[0]["region"]) if len(r2) else "N/A"
    top_cont = str(r3.iloc[0]["contaminante"]) if len(r3) else "N/A"
    share_top = float(r4.iloc[0]["share_top"]) if len(r4) else 0.0

    print("\n=== Summary ===")
    print(f"- Años cubiertos: {anio_min}–{anio_max}")
    print(f"- Región #1 (acumulado): {top_region}")
    print(f"- Contaminante #1 (acumulado): {top_cont}")
    print(f"- Concentración top 5% emisores: {share_top:.2%}")


if __name__ == "__main__":
    main()

