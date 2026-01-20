# Schema Mapping - Esquema Canónico v1
### Proyecto : Environmental Data Platform - End-to-End Emissions Analytics

#### Autor : Eduardo S. Henríquez N.
#### Fecha : 19 / 01 / 26.

## 1. Descripción general.

Los datos de emisiones al agua de contaminantes utilizados en esta plataforma provienen de fuentes públicas oficiales y abarcan un período extenso (2005–2026). A lo largo de estos años, el modelo de datos original ha experimentado cambios estructurales significativos, tanto en la forma de nombrar columnas como en el nivel de normalización, granularidad y uso de identificadores.

En particular, se identifican tres generaciones de esquema:

- **2005-2017** : Un modelo con encabezados descriptivos, uso de acentos y espacios, ausencia de identificadores normalizados y algunas limitantes técnicas.
- **2018-2023** : Una transición hacia esquemas más técnicos *snake case*, incorporación progresiva de identificadoresy métricas más estandarizadas, aunque con inconsistencias de *encoding* y variaciones menores entre cada año.
- **2024-2026** : Un modelo más vanguardista y normalizado, con separación clara entre dimensiones, uso sistémico de IDs, métricas consolidadas y mayor preparación para consumo analítico.

Debido a esta evolución, no es posible ni deseable unificar estos datasets mediante una unión directa. Por esta razón se define un esquema canónico v1, que actúa como contrato de datos estable en la capa *Staging*.
Este esquema:

- **Preserva la información esencial de todos los períodos.**

- **Permite la coexistencia de datos legacy y modernos.**

- **Unifica métricas clave (por ejemplo, emisiones en toneladas) bajo un único nombre semántico.**

- **Normaliza nombres, tipos y encoding.**

- **Documenta explícitamente las ausencias o limitaciones históricas, en lugar de ocultarlas.**  


## 2. Convenciones generales.

- **Nombre en *snake_case*, sin acentos**
- **Tipos lógicos normalizados.**
- **IDs tratados como *string*.**
- **Métrica única canónica para emisiones: *emision_toneladas***
- **Valores no disponibles en ciertos períodos se representan como *NULL***
- **Encoding normalizado a UTF-8 en *Staging*.**
 
## 3. Esquemas identificados.
<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px;">Período</th>
    <th style="border: 3px solid black; padding: 8px;">Características</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;">2005-2017</td>
    <td style="border: 3px solid black; padding: 8px;">Header no técnicos, acentos, espacios, sin IDs normalizados</td>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;">2018-2023</td>
    <td style="border: 3px solid black; padding: 8px;"><i>snake_case</i>, IDs explícitos, encoding inconsistente</td>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;">2024-2026</td>
    <td style="border: 3px solid black; padding: 8px;">Esquema moderno, normalizado, consistente</td>
  </tr>
</table>


## 4. Esquema canónico v1 y mapeo por período.
### 4.1. Metadatos de plataforma

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Notas</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>source_file</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>generado</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>generado</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>generado</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Nombre archivo Raw</i></td>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>fecha_ingestion</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>date</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>generado</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>generado</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>generado</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>fecha de carga</i></td>
  </tr>
</table>
<br>
### 4.2. Tiempo

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Notas</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>anio</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>int</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Año</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>año/a�o</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>año</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Normalización de encoding</i></td>
  </tr>
</table>
<br>
### 4.3. Identidad del establecimiento.

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>razon_social</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Razón social</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>razon_social</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>razon_social</i></td>
  </tr>
   <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>rut_razon_social</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>rut_razon_social</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>rut_razon_social</i></td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>nombre_establecimiento</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Nombre de establecimiento</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>nombre_establecimiento</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>nombre_establecimiento</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>id_vu</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ID establecimiento(VU)</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_vu</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_vu</i><td>

  </tr>
</table>
<br>
### 4.4. Clasificación económica.

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu4</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>CIIU4</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu4</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu4</i></td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu4_id</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_ciiu4</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu4_id</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu6</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu6</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu6</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu6_id</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_ciiu6</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ciiu6_id</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>rubro</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Rubro RETC</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>rubro_vu</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>rubro</i><td>
  </tr>

 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>rubro_id</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_rubro_vu</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>rubro_id</i><td>
  </tr>

</table>
<br>
### 4.5. Geografía.

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>region</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Región</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>region</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>region</i></td>
  </tr>
   <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>provincia</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Provincia</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>provincia</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>provincia</i></td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>comuna</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Comuna</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>comuna/comuna_</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>comuna</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>codigo_territorial</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_comuna</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>codigo_unico_territorial</i><td>

  </tr>
</table>
<br>
### 4.6. Identidad del establecimiento.

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Notas</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>latitud</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>float</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>latitud</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>latitud</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>longitud</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>float</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>longitud</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>longitud</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>(legacy)</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Coordenada norte/este</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>No transformado en v1</i></td>
  </tr>
</table>
<br>

### 4.7. Emisión(núcleo analítico)
<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>emision_toneladas</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>float</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Emisión(toneladas)</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>cantidad_toneladas</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>emision_total</i></td>
  </tr>
   <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>contaminante</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Tipo de Contaminante</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>contaminantes</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>contaminante</i></td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>contaminante_id</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>id_contaminante</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>contaminante_id</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>norma</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Norma</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>norma</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>norma</i><td>
  </tr>
 <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>origen</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>origen</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>origen</i><td>
  </tr>

</table>
<br>
### 4.8. Infraestructura

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2005-2017</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2023</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2024-2026</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>ducto</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>Ducto</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ducto</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ducto</i></td>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>nombre_ducto</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>-</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>nombre_ducto</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>ducto_nombre</i></td>
  </tr>
</table>
<br>
### 4.9. Campo técnico.

<table style="border: 3px solid black; border-collapse: collapse;">
  <tr>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Columna canónica</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">Tipo</th>
    <th style="border: 3px solid black; padding: 8px; background-color: #f2f2f2;">2018-2026</th>
  </tr>
  <tr>
    <td style="border: 3px solid black; padding: 8px;"><i>tabla</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>string</i></td>
    <td style="border: 3px solid black; padding: 8px;"><i>tabla</i></td>
  </tr>
</table>

## 5. Reglas de transformación en STAGING

Durante la capa *staging*, los datos deben ajustarse al esquema canónico definido, aplicando las siguientes reglas:

- **Normalización de encoding y nombres de columnas para asegurar consistencia(por ejemplo, corrección de caracteres mal codificados como a�o a anio)**

- **Unificación de las métricas de emisión en una única columna semántica(emision_toneladas), independiente del nombre original utilizado en cada período**

- **Conversión explicita de tipos de datos:**
    - ***anio como entero***
    - ***emision_toneladas como valor flotante***
    - ***Identificadores tratados como cadenas de texto para evitar inconsistencias históricas***

- **Incorporación de metadatos de trazabilidad(source_file, fecha_ingestion) generados durante el proceso de carga**

- **Se mantendrá respeto estricto por los datos originales: los campos no disponibles en períodos legacy se mantienen como valores nulos y no se infieren ni completan artificialmente**
 
## 6. Alcance del esquema.

Cualquier cambio estructural futuro deberá introducirse mediante una nueva versión del esquema, conservando compatibilidad y trazabilidad entre versiones (v2, v3, etc) 
