# Data Quality Validation (STAGING)
### Proyecto : Environmental Data Platform - End-to-End Emissions Analytics 
#### Autor : Eduardo S. Henríquez N.  
#### Fecha : 19 / 01 / 26.

## Descripción General

Este documento describe las validaciones de calidad aplicadas a la capa *staging* del proyecto Environmental Data Platform, cuyo objetivo es garantizar que el dataset unificado de emisiones cumpla con el esquema canónico v1 y sea consistente, trazable y apto para su consumo analítico.

Las validaciones se realizaron sobre datos históricos comprendidos entre los años 2005 y 2026, provenientes de fuentes públicas oficiales de la Subsecretaría del Medio Ambiente.

---

## Dataset Evaluado

- **Nombre:** `emisiones_staging.parquet`
- **Capa:** STAGING
- **Cobertura temporal:** 2005 – 2026
- **Dominio:** Emisiones al agua de cuerpos contaminantes

---

## Validaciones Realizadas

Durante el proceso de validación se ejecutaron los siguientes controles:

- Verificación del conteo total de filas y columnas.
- Validación del cumplimiento del esquema canónico v1.
- Revisión de tipos de datos para campos críticos.
- Análisis básico de valores nulos por columna.
- Validación de trazabilidad mediante el campo `source_file`.

---

## Resultados

### Estructura del Dataset
- **Filas totales:** 178.963
- **Columnas:** 27 (esquema canónico v1)

### Tipos de Datos Críticos
- `anio`: Int64 (nullable)
- `emision_toneladas`: float
- Identificadores normalizados como `string`
- Coordenadas geográficas como `float`

### Valores Nulos
Los valores nulos observados corresponden a condiciones esperadas y documentadas:

- Campos de coordenadas (`latitud`, `longitud`) ausentes en períodos legacy (2005–2017).
- Campos como `tabla`, `origen` y `nombre_ducto` no disponibles en todos los años.
- Clasificaciones económicas (`ciiu6`, `ciiu6_id`) incorporadas a partir de años posteriores.

No se detectaron patrones anómalos ni inconsistencias críticas.

### Distribución por Archivo de Origen
- `2005-2017`: 104.863 registros  
- `2018-2026`: 74.100 registros (distribuidos por año)

---
<br>
## Conclusión

El dataset `emisiones_staging.parquet` cumple satisfactoriamente con los criterios de calidad definidos para la capa *staging*.  
Los resultados obtenidos son coherentes con la evolución histórica de los datos y con las decisiones de diseño documentadas en el esquema canónico.

Por tanto este dataset se considera apto para su uso en capas analíticas, modelado de datos y visualización dentro de la plataforma.

---

