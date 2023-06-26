# Film Recommendation Model

## - Proyecto: Desarrollar e implementar un modelo de recomendación de películas, usar FastApi y montarla en Render, previamente realizar ETL y EDA sobre los datasets originales.

## Requerimientos:
Desarrollado en Python:
Librerias: FastApi, Pandas, Numpy, Skitlearn, Seaborns, Scipy, Seaborn, Uvicorn, Wordcloud, Matplotlib.

Estructura de carpetas
1. Data: Esta carpeta guarda los datasets del proyecto.
2. Documentation: Esta carpeta guarda el diccionario de datos.
3. Notebooks: Esta carpeta guarda los notebooks del ETL y EDA.
4. model/enntorno_frmodel: Esta carpeta guarda las dependencias del proyecto.
5. main.py: Archivo de Python que gestiona la aplicación del modelo.
6. requirements.txt: Este archivo guarda las librerias del proyecto.

### Instrucciones de Ejecución
Para disponibilizar los datos es necesario:
a) Correr previamente el notebook etl.ipynb, el cual extrae y transforma los datatasets originales.
b) Ejecutamos el notebook eda.ipynb donde buscamos la relación entre el budget y la revenue, analizamos los datos atípicos con la variable popularity, por último generamos una nube de palabras de la columna 'title'.

### API endpoints
Aplicación montada en Render:
https://film-recommendation-model-nzqm.onrender.com/

**/cantidad_filmaciones_mes/{mes}** retorna la cantidad de peliculas que se estrenaron en ese mes historicamente, ejemplo: enero / febrero / marzo, etc.
**/cantidad_filmaciones_dia/{dia}** retorna la cantidad de peliculas que se estrenaron en ese día historicamente, ejemplo: lunes / martes / miercoles, etc.
 **/score_titulo/{titulo}** ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score, ejemplo: /score_titulo/toy story
**/votos_titulo/{titulo}** ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones, deberá de contar con al menos 2000 valoraciones para mostrar resultados, ejemplo /votos_titulo/Jumanji
 **/get_actor/{nombre_actor}**  ingresa nombre de actor para devolver el éxito a través del retorno y cantidad de películas que participó y el promedio de retorno, ejemplo: /get_actor/Salma Hayek
**/get_director/{nombre_director}** ingresa nombre de director para devolver el éxito del mismo medido a través del retorno, nombre de sus películas, con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, ejemplo: /get_director/Martin Scorsese
**/recomendacion/{titulo}** Ingresas un nombre de pelicula y te recomienda las similares en una lista, ejemplo /recomendacion/tomorrow

### Análisis exploratorio de datos
**Destacamos la relación entre el budget y la revenue**:
[![Relación entre budget y revenue](https://github.com/renarzamora/Film-recommendation-model/blob/master/Graficos/budget-revenue.png?raw=true "Relación entre budget y revenue")
**
Analizamos los datos atípicos con la variable popularity.**
![Outliers de la variable popularity](https://github.com/renarzamora/Film-recommendation-model/blob/master/Graficos/boxplot-popularity.png?raw=true "Outliers de la variable popularity")

**Nube de palabras de la columna 'title'**
![Bube de palabras](https://github.com/renarzamora/Film-recommendation-model/blob/master/Graficos/nube-de-palabras.png?raw=true "Bube de palabras")

### Sistema de recomendación
Ingresamos un nombre de pelicula y te recomienda las similares en una lista, ordenas en forma descendente por score.
Utilizamos una matriz TF-IDF para representar los títulos de las películas con TfidfVectorizer y hacemos el entrenamiento con la columna title.
Calculamos la similitud coseno entre la búsqueda y los títulos de las películas, cosine_similarity nos da la similitud de películas, volcamos el resultado en un dataframe y los ordenamos por la columna score de forma descendente y retornamos los 5 primeros registros.

### Video de demostración

### Autor
Renar zamora
renarzamora@gmail.com
