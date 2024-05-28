## Proyecto Integrador #1 MLOPS

![alt text](image.png)
### Contenido
- [Planteamiento del problema](#planteamiento-del-problema)
- [DataSets](#datasets)
- [Explicación del repositorio](#explicación-del-repositorio)
- [Links](#links)
- [Recursos](#recursos)

### Planteamiento del problema
En este proyecto se nos propone emular el ciclo de vida de un proyecto de ML, por lo que se tocan las diferentes etapas de este ciclo, desde el proceso de ETL de los datos, el análisis y preparación de los datos hasta el montaje del modelo final. Además, se nos propone disponibilizar los datos usando el framework FastAPI. Las consultas que se deben implementar son las siguientes:

- **def developer( desarrollador: str ):** Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
- **def userdata( User_id: str ):** Debe devolver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
- **def UserForGenre( genero: str ):** Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
- **def best_developer_year( año: int ):** Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado (reviews.recommend = True y comentarios positivos).
- **def developer_reviews_analysis( desarrolladora: str ):** Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

Una vez desarrollados los endpoints anteriores, también se nos propone entrenar nuestro modelo de machine learning para armar un sistema de recomendación. Para ello, se ofrecen dos propuestas de trabajo: 

1. **Sistema de recomendación ítem-ítem:** Toma un ítem y, en base a su similitud con otros ítems, recomienda ítems similares. Aquí el input es un juego y el output es una lista de juegos recomendados.
2. **Sistema de recomendación usuario-ítem:** Toma un usuario, encuentra usuarios similares y recomienda ítems que a esos usuarios les gustaron. En este caso, el input es un usuario y el output es una lista de juegos recomendados para ese usuario.

Para el desarrollo del sistema de recomendación se ha usado la Similitud del coseno. 

- **Sistema de recomendación ítem-ítem:**
  - **def recomendacion_juego( id de producto ):** Ingresando el id de producto, se recibe una lista con 5 juegos recomendados similares al ingresado.
- **Sistema de recomendación usuario-ítem:**
  - **def recomendacion_usuario( id de usuario ):** Ingresando el id de un usuario, se recibe una lista con 5 juegos recomendados para dicho usuario.

### DataSets
Cabe aclarar que los datasets que se explican son el resultado de los procesos de ETL realizados a los datasets originales (los cuales no se encuentran en el repositorio por fines prácticos, pero su proceso de ETL está explicado en la carpeta denominada 'ETL').

- **Items.csv:** Contiene las siguientes columnas:
  - item_id: ID del juego
  - item_name: Nombre del juego
  - playtime_forever: Tiempo total jugado por el usuario
  - users_id: ID del usuario
  - items_count: Cantidad de ítems (juegos) que tiene el usuario

- **Reviews.csv:** Contiene las siguientes columnas:
  - item_id: ID del juego
  - senti_negativo: Cantidad de reviews negativas del juego
  - senti_neutral: Cantidad de reviews neutrales del juego
  - senti_positivo: Cantidad de reviews positivas del juego

- **steam_games.csv:** Contiene las siguientes columnas:
  - app_name: Nombre del juego
  - price: Precio del juego
  - id: ID del juego
  - developer: Desarrolladora del juego
  - principal_genre: Género principal del juego
  - principal_tag: Etiqueta principal del juego
  - principal_spec: Especificación principal del juego
  - release_year: Año de lanzamiento del juego

- **user_reviews.csv:** Contiene las siguientes columnas:
  - user_id: ID del usuario
  - recommend_yes: Cuántas veces ha sido recomendado
  - recommend_not: Cuántas veces ha sido no recomendado

### Explicación del repositorio
En este apartado se explica cómo está estructurado este repositorio:

- **Carpeta Data:** Contiene los archivos con los datos que se usan para el desarrollo del proyecto.
- **Carpeta ETL:** Aquí se encuentran los notebooks donde se realizó el proceso de ETL a cada uno de los archivos donde se encontraban los datos inicialmente. En cada uno de los notebooks se explica paso a paso el proceso realizado a cada base de datos.
- **fasApi-env:** Es el entorno virtual donde se hicieron las pruebas locales de la API.
- **EDA.ipynb:** Este notebook contiene un breve análisis de los datos resultantes de los procesos de ETL.
- **EndPoint.ipynb:** En este notebook están los endpoints explicados y cómo es su funcionalidad.
- **Main.py:** Es el archivo donde se encuentra el cuerpo de la API, con los endpoints desarrollados.
- **Requirements.txt:** Librerías requeridas para hacer el deploy.

### Links 
- [Mira el modelo aquí](https://proyecto-individual-1-mlops-9639.onrender.com/docs)
- [Video de explicación](https://drive.google.com/drive/folders/1U92josASB70qRucss6RobAwH_hrTxT9i?usp=sharing)

### Recursos
- [Cómo funciona la búsqueda de similitud](https://pro.arcgis.com/es/pro-app/latest/tool-reference/spatial-statistics/how-similarity-search-works.htm#:~:text=El%20%C3%ADndice%20de%20similitud%20de%20coseno%20oscila%20entre%201%2C0,una%20mayor%20o%20menor%20escala.)
