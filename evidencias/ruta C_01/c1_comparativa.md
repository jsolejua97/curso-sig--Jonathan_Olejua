# C1. Repaso de estándares SIG con servicios reales

## 1. Objetivo

Identificar las diferencias entre los principales estándares y servicios utilizados para publicar y consultar información geográfica en la web, mediante la revisión de un servicio WMS del DANE, un servicio ArcGIS FeatureServer y una colección de OGC API Features.

## 2. Consulta del WMS del DANE

**Servicio consultado:** [WMS del DANE - MGN 2024](https://geoportal.dane.gov.co/mparcgis/services/MGN2024/Serv_CapasMGN_2024/MapServer/WMSServer?service=WMS&request=GetCapabilities)

Para revisar las capacidades del servicio, se abrió la solicitud `GetCapabilities`, que devuelve un documento XML con información sobre las capas disponibles, los sistemas de referencia y las operaciones admitidas.

### Resultados obtenidos

Se identificaron **10 capas de datos**:

1. Manzana.
2. Sección Urbana.
3. Sector Urbano.
4. Sección Rural.
5. Sector Rural.
6. Clase.
7. Zona Urbana.
8. Municipio.
9. Departamento.
10. País.

La capa raíz `Serv_CapasMGN_2024` funciona como agrupación de las capas anteriores y no se contó como una capa de datos adicional.

Los sistemas de referencia anunciados en el XML revisado fueron:

- `CRS:84`
- `EPSG:4326`
- `EPSG:3857`
- `EPSG:102100`

Estos son cuatro identificadores de CRS. `EPSG:3857` y `EPSG:102100` están asociados con la proyección Web Mercator.

### ¿Qué entrega un WMS?

El estándar Web Map Service (WMS) entrega imágenes cartográficas georreferenciadas, por ejemplo, en formatos PNG o JPEG. No está diseñado principalmente para descargar las geometrías vectoriales completas de cada entidad.

Sus operaciones principales incluyen:

- `GetCapabilities`: consulta las capacidades y las capas disponibles.
- `GetMap`: solicita una imagen del mapa.
- `GetFeatureInfo`: permite consultar información de entidades representadas en una ubicación, cuando el servicio admite esta operación.

## 3. Consulta de tres veredas mediante ArcGIS FeatureServer

**Servicio consultado:** [Veredas de Boyacá - FeatureServer](https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query?where=1%3D1&outFields=*&resultRecordCount=3&f=geojson)

La consulta utilizó los siguientes parámetros:

- `where=1=1`: solicita entidades sin aplicar un filtro restrictivo por atributos.
- `outFields=*`: solicita todos los campos disponibles.
- `resultRecordCount=3`: establece una cantidad solicitada de tres registros.
- `f=geojson`: solicita la respuesta en formato GeoJSON.

### Resultados obtenidos

La respuesta presentó una estructura de tipo `FeatureCollection` y tres entidades geográficas con geometría `Polygon`.

| Vereda | Municipio | Departamento | Área reportada (ha) |
|---|---|---|---:|
| La Lajita | Tunja | Boyacá | 242,10 |
| La Hoya | Tunja | Boyacá | 809,74 |
| Baron | Tunja | Boyacá | 1.185,20 |

Entre los atributos identificados se encuentran `NOMBRE_VER`, `CODIGO_VER`, `NOMB_MPIO`, `NOM_DEP`, `AREA_HA` y `FUENTE`.

### Estructura de la respuesta

- `type`: identifica el tipo de objeto GeoJSON; en el nivel principal aparece `FeatureCollection`.
- `features`: contiene las entidades devueltas.
- `geometry`: almacena el tipo de geometría y sus coordenadas.
- `properties`: contiene los atributos descriptivos de cada entidad.

La respuesta también incluyó `exceededTransferLimit: true`. Este indicador advierte sobre un límite de transferencia del servicio; por ello, no se debe asumir que la consulta representa la totalidad de las entidades disponibles.

## 4. Consulta de tres elementos mediante OGC API Features

**Servicio consultado:** [Colección lakes de pygeoapi](https://demo.pygeoapi.io/master/collections/lakes/items?limit=3&f=json)

La colección `lakes` se utilizó para comparar la estructura de la respuesta con la del FeatureServer. Esta colección contiene lagos, no veredas.

El parámetro `limit=3` solicita hasta tres elementos por respuesta.

### Resultados obtenidos

Se recibieron tres entidades:

1. Lake Baikal.
2. Lake Winnipeg.
3. Great Slave Lake.

La respuesta presentó una estructura `FeatureCollection`, con elementos de tipo `Feature`, geometrías `Polygon` y atributos como `id`, `name` y `featureclass`.

También se identificaron los siguientes campos:

- `numberMatched: 25`: número de elementos coincidentes informado por el servicio.
- `numberReturned: 3`: cantidad de elementos devueltos en la respuesta.
- `links`: conjunto de enlaces relacionados con el recurso.
- `rel: next`: identifica el enlace para consultar la siguiente página.

La respuesta demuestra que el servicio permite solicitar una cantidad limitada de elementos y proporciona un enlace de navegación para continuar la consulta.

## 5. Comparación de la estructura JSON

| Característica | ArcGIS FeatureServer | OGC API Features |
|---|---|---|
| Formato consultado | GeoJSON | GeoJSON |
| Tipo principal | `FeatureCollection` | `FeatureCollection` |
| Elementos devueltos | 3 veredas | 3 lagos |
| Tipo de entidad | `Feature` | `Feature` |
| Geometría observada | `Polygon` | `Polygon` |
| Atributos | Códigos, nombres, municipio, departamento, área y fuente | Identificador, nombre y clase del elemento |
| Información de paginación observada | `exceededTransferLimit: true` | `numberMatched`, `numberReturned` y enlace `next` |
| Parámetro usado para limitar resultados | `resultRecordCount=3` | `limit=3` |

### Interpretación

Las dos respuestas comparten la estructura GeoJSON: una colección contiene entidades, y cada entidad incluye geometría y atributos. Esto facilita su integración con aplicaciones SIG web y bibliotecas cartográficas.

La diferencia está en los parámetros de consulta y en la información adicional que proporciona cada servicio. En el ejemplo de pygeoapi, los campos `numberMatched`, `numberReturned` y el enlace `next` permiten identificar los resultados y continuar la navegación. En el FeatureServer se observó el indicador `exceededTransferLimit`, que debe interpretarse teniendo en cuenta las reglas de transferencia de ese servicio.

## 6. Tabla comparativa de estándares y servicios

| Servicio | ¿Qué entrega? | ¿Cómo se filtra? | ¿Cómo se pagina? |
|---|---|---|---|
| **WMS** | Imágenes cartográficas georreferenciadas. | Se seleccionan capas y parámetros espaciales de representación. Algunas implementaciones admiten consultas de información mediante `GetFeatureInfo`. | La paginación de entidades no es su mecanismo habitual; se solicitan mapas para áreas, escalas o extensiones específicas. |
| **WFS** | Entidades vectoriales con geometrías y atributos. | Mediante consultas `GetFeature` y filtros de atributos o espaciales, según la versión y las capacidades del servidor. | Depende de la versión y del soporte del servidor. WFS 2.0 contempla parámetros como `count` y `startIndex`. |
| **ArcGIS FeatureServer** | Entidades y atributos mediante una API REST; puede responder en GeoJSON. | Utiliza parámetros como `where`, `outFields` y, según el servicio, filtros espaciales. | Puede utilizar `resultRecordCount` y `resultOffset`, respetando los límites configurados por el servicio. |
| **OGC API Features** | Entidades geográficas y sus propiedades mediante una API web. | Puede admitir filtros de atributos y espaciales, según las capacidades implementadas y las extensiones disponibles. | Puede usar `limit`, `offset` y enlaces de navegación como `next`, según la implementación. |

**Nota:** las opciones concretas de filtrado y paginación dependen de la versión, las capacidades y la configuración del servidor. La tabla resume los mecanismos habituales; no implica que todos los servicios admitan todas las opciones.

## 7. Diferencias entre los estándares

WMS se orienta a la visualización de cartografía mediante imágenes. WFS permite acceder directamente a entidades vectoriales y sus propiedades. WMTS publica mapas mediante teselas o *tiles* previamente preparadas, facilitando su visualización eficiente.

ArcGIS FeatureServer utiliza una API REST del ecosistema ArcGIS para consultar entidades mediante rutas y parámetros específicos. OGC API Features es un estándar OGC basado en una interfaz web moderna para acceder a entidades geográficas.

Los servicios OGC tradicionales suelen utilizar operaciones como `GetCapabilities`, mientras que las API REST y OGC API Features emplean rutas y parámetros HTTP para consultar recursos. Sin embargo, ambos enfoques pueden intercambiar información geográfica y utilizarse desde aplicaciones web.

## 8. Conclusiones

La consulta de servicios geográficos permite identificar diferencias en el tipo de información entregada y en los mecanismos para acceder a ella. WMS es apropiado para visualizar mapas, mientras que WFS, ArcGIS FeatureServer y OGC API Features permiten consultar entidades y atributos.

Las dos consultas vectoriales realizadas devolvieron información GeoJSON con geometrías poligonales y atributos. No obstante, el FeatureServer y OGC API Features utilizan parámetros y mecanismos de paginación diferentes. Por esta razón, al integrar servicios en una aplicación SIG web es importante revisar su documentación, sus capacidades y la estructura de sus respuestas.

## 9. Fuentes consultadas

- DANE. Servicio WMS del Marco Geoestadístico Nacional 2024.
- ArcGIS REST API. Servicio FeatureServer de veredas de Boyacá.
- pygeoapi. Colección `lakes` de la demostración de OGC API Features.
- Open Geospatial Consortium (OGC). Estándares Web Map Service (WMS) y Web Feature Service (WFS).
- Esri Developer. Documentación de consultas y paginación de Feature Services.
