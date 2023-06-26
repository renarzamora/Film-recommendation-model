import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
from datetime import datetime
import os

app = FastAPI()

dir_actual = os.getcwd()+'/Data/' 


@app.get("/")
def index():
    cfun1 = ["para retornar la cantidad de peliculas que se estrenaron ese mes historicamente /cantidad_filmaciones_mes/{mes}"]
    cfun2 = ["para retornar la cantidad de peliculas que se estrenaron ese dia historicamente /cantidad_filmaciones_dia{dia}"]
    cfun3 = ["ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score /score_titulo/{titulo}"]
    cfun4 = ["ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones /votos_titulo/{titulo}"]
    cfun5 = ["ingresa nombre de actor para devolver el éxito a través del retorno y cantidad de películas que participó y el promedio de retorno /get_actor/{nombre_actor"]  
    cfun6 = ["ingresa nombre de director para devolver el éxito del mismo medido a través del retorno, nombre de sus películas, "]
    cfun6 = cfun6 + ["con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. /get_director(nombre_director)"]
    cfun7 = ['Ingresas un nombre de pelicula y te recomienda las similares en una lista. /recomendacion/{titulo}']

    milista = cfun1+cfun2+cfun3+cfun4+cfun5+cfun6+cfun7
    return milista
              
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    qmes=mes.lower()
    meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    if qmes in meses:
        nmes = meses.index(qmes) + 1
    else:
        nmes=0    
    
    nmes = 9 if 'setiembre' in mes else nmes
    
    if nmes == 0:
        respuesta = {'No corresponde a un mes del año'}
        return respuesta  
    
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')
    df_movies["release_month"] = df_movies["release_date"].apply(lambda x: x[5:7]).astype('int')
    respuesta = df_movies.loc[df_movies["release_month"] == nmes].shape[0]
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    return {'mes':mes, 'cantidad':str(respuesta)}


@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    qdia=dia.lower()
    dias=['lunes','martes','miercoles','jueves','viernes','sabado','domingo']
    if qdia in dias:
        ndia = dias.index(qdia)
    else:
        respuesta = {'No corresponde a un día de la semana'}
        return respuesta   
   
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')
    df_movies["release_date"] = pd.to_datetime(df_movies["release_date"], infer_datetime_format=False)
    df_movies["release_day"] = df_movies["release_date"].dt.weekday
    respuesta = df_movies.loc[df_movies["release_day"] == ndia].shape[0]
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia historicamente'''
    return {'dia':dia, 'cantidad':str(respuesta)}

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    titulo = titulo.lower()
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')
    df_movies["title"] = df_movies["title"].str.lower()
    df_query = df_movies[df_movies["title"].str.contains(titulo)]
    tot_sel=df_query['title'].count()
    if tot_sel == 0:
        return {'No se encontraron películas similares al título ingresado'}
    
    titulo=df_query['title'].iloc[0]
    titulo=titulo.title()
    anio = df_query['release_year'].astype('str').iloc[0]
    popularidad = df_query['popularity'].iloc[0]
    
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    return {'titulo':titulo, 'anio':anio, 'popularidad':popularidad}

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    titulo = titulo.lower()
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')
    df_movies["title"] = df_movies["title"].str.lower()
    
    df_query = df_movies[df_movies["title"] == titulo]
    tot_sel = df_query['title'].count() # revisa si el query devolvió datos
    
    if tot_sel < 1:
        return {'No se encontraron películas similares al título ingresado'}
    
    valoracion = df_query["vote_count"].iloc[0]
    
    if valoracion < 2000:
        return {'La película no cumple con las 2000 o más valoraciones requeridas'}
    
    titulo=titulo.title()
    anio = df_query['release_year'].iloc[0]
    promedio = df_query['vote_average'].iloc[0]
    
                
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    return {'titulo':titulo, 'anio':str(anio), 'voto_total':valoracion, 'voto_promedio':promedio}

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    nombre_actor = nombre_actor.lower() #convierto en minuscula la variables
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')
    df_movies = df_movies.rename(columns={"id": "id_film"}) # renombro la columna id

    df_casting = pd.read_csv(dir_actual+'casting_final.csv')
    df_casting["name_actor"] = df_casting["name_actor"].str.lower() #convierto en minuscula la columna
        
    df_total=pd.merge(df_movies, df_casting, on = 'id_film', how = 'inner')

    df_query = df_total[df_total["name_actor"].str.contains(nombre_actor)]
    tot_sel=df_query['name_actor'].count()
    
    if tot_sel == 0:
        return {'No se encontraron películas para el nombre de actor ingresado'}
    
    nombre_actor = nombre_actor.title()
    retorno_total = df_query['roi'].sum()
    retorno_promedio = df_query['roi'].mean()
    
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    return {'actor':nombre_actor, 'cantidad_filmaciones':str(tot_sel), 'retorno_total':str(retorno_total), 'retorno_promedio':str(retorno_promedio)}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
 
    nombre_director = nombre_director.lower() #convierto en minuscula la variables
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')
    df_movies = df_movies.rename(columns={"id": "id_film"}) # renombro la columna id

    df_directors = pd.read_csv(dir_actual+'directors_final.csv')
    df_directors["name_director"] = df_directors["name_director"].str.lower() #convierto en minuscula la columna
        
    df_total=pd.merge(df_movies, df_directors, on = 'id_film', how = 'inner')

    df_query = df_total[df_total["name_director"].str.contains(nombre_director)]
    tot_sel=df_query['name_director'].count()
    
    if tot_sel == 0:
        return {'No se encontraron películas para el nombre de director ingresado'}
    
    nombre_director = nombre_director.title()
    
    retorno_total = df_query['roi'].sum()
    

   
    diccio_retorna={}
    diccio_retorna['director'] = nombre_director
    diccio_retorna['retorno_total_director'] = str(retorno_total)
    
    for ind_peli in range(0,tot_sel):
        diccio_retorna['pelicula'+str(ind_peli)] = [
                {"titulo": df_query['title'].iloc[ind_peli], 
                'anio':str(df_query['release_year'].iloc[ind_peli]), 
                'retorno_pelicula':str(df_query['roi'].iloc[ind_peli]), 
                'budget_pelicula':str(df_query['budget'].iloc[ind_peli]), 
                'revenue_pelicula':str(df_query['revenue'].iloc[ind_peli])}
                ]
    return diccio_retorna
    
    #return {'director':nombre_director, 'retorno_total_director':respuesta, 
    #'peliculas':respuesta, 'anio':respuesta, 'retorno_pelicula':respuesta, 
    #'budget_pelicula':respuesta, 'revenue_pelicula':respuesta}

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    # Leer el archivo CSV y convertirlo en un DataFrame
    df_movies = pd.read_csv(dir_actual+'movies_final.csv')

    search_word = titulo
    # Crear un nuevo dataframe df_movies_final eliminando las filas con budget igual a 0
    df_movies_final = df_movies[df_movies['budget'] != 0]

    # Función para realizar el entrenamiento y obtener las recomendaciones
    def get_recommendations(search_word, df):
        # Crear una matriz TF-IDF para representar los títulos de las películas
        stopwords = {["to", "of", "the", "and", "&", ":", "in", "for", "on", "a", "by", "with", "an", "into", "from"]}
        tfidf_vectorizer = TfidfVectorizer(stopwords)
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['title'])
    
        # Calcular la similitud coseno entre la búsqueda y los títulos de las películas
        search_vector = tfidf_vectorizer.transform([search_word])
        similarity_scores = cosine_similarity(search_vector, tfidf_matrix).flatten()
    
        # Agregar los resultados al dataframe y ordenarlos por puntuación en forma descendente
        df['score'] = similarity_scores
        df = df.sort_values(by='score', ascending=False)
    
        # Filtrar los 5 primeros resultados y agregarlos al diccionario de resultados
        result_dict = {}
        for i in range(5):
            result_dict[df.iloc[i]['title']] = df.iloc[i]['score']
    
        return result_dict

    # Realizar la búsqueda y obtener los resultados para la palabra clave 'Live'
    #search_word = titulo
    dic_resultado = get_recommendations(search_word, df_movies_final)

    # Mostrar los resultados
    total = sum(dic_resultado.values())

    dic_resultado = {'No se encontaron resultado'} if total == 0 else dic_resultado 

    dic_resultado = dic_resultado if total > 0 else {'No se encontaron resultado'}

    return dic_resultado