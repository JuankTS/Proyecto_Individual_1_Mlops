# Librerias 
from fastapi import FastAPI, Query
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Datos
items = pd.read_csv('./Data/items.csv')
reviews = pd.read_csv('./Data/Reviews.csv')
games = pd.read_csv('./Data/steam_games.csv')
users = pd.read_csv('./Data/Users.csv')

# Inicio de la app
app= FastAPI(title='Proyecto Integrador #1 Presentado por Juan Camilo Torres')

@app.get('/',tags=['Home'])

async def Home():
    return 'Bienvenidos a la API del Proyecto Individual #1'

@app.get('/about', tags=['About this Proyect'])
async def about():
    return 'PROYECTO INDIVIDUAL #1 Machine Learning Operations (MLOps) presentado por Juan Camilo Torres Salas'

@app.get('/Developer', tags=['GET'])
def developer(desarrollador : str = Query(default='xropi,stev3ns')):
    
    ''' Ingresa una desarrolladora y te retorna la cantidad de juegos por año y el porcentaje 
    
    de esos juegos que son gratis'''
    filter_games=games[games['developer']== desarrollador]
    filter_games=filter_games.groupby('release_year').agg(Cantidad_de_Items=('app_name', 'size'),
                                             free_games=('price', lambda x: (x == 0.0).sum())).reset_index()
    filter_games['Contenido Free']= round((filter_games['free_games']/filter_games['Cantidad_de_Items'])*100, 3)
    
    dic = {}
    for _, row in filter_games.iterrows():
        año = row['release_year']
        cantidad_items = row['Cantidad_de_Items']
        cont_free = row['Contenido Free']
        
        dic[int(año)] = {
            'Cantidad de items': int(cantidad_items),
            'Contenido Free': cont_free
        }
    
    return dic

@app.get('/UserData', tags=['GET'])
def userdata( User_id : str= Query(default='kube134')):
    
    '''Ingresa el ID de usuario y te retorna infromacion sobre el usario'''
    
    game=games[['id', 'price']]
    user= users[users['user_id']== User_id]
    
    por_recommed= round((user['recommend_yes']/(user['recommend_yes']+user['recommend_not']))*100,2).iloc[0] 
    
    item_filter= items[items['users_id']==User_id]
    item_filter= item_filter.merge(game, left_on='item_id', right_on='id', how='inner')
    item_filter= item_filter.groupby('users_id').agg({'playtime_forever':'sum',
                                                      'price':'sum'}).reset_index()
    
    usuario= item_filter['users_id'].iloc[0]
    tiempo= item_filter['playtime_forever'].iloc[0]
    dinero= item_filter['price'].iloc[0]
    
    return {'Usuario': usuario, 'Dinero invertido': round(dinero,2), 'Tota horas de juego': tiempo,"% de recomendación":por_recommed}

@app.get('/UserForGenre', tags=['GET'])
def UserForGenre(genre: str=Query(default='Indie')):
    
    '''Ingresa un género de video juegos y te retorna el usuario con mas hora jugadas de ese género'''
    
    item = items[['item_id', 'playtime_forever', 'users_id']]
    game = games[['id', 'principal_genre', 'release_year']]
    game = game[game['principal_genre'] == genre]
    
    filter_game = game.merge(item, left_on='id', right_on='item_id', how='inner')
    
    user_year= filter_game.groupby(['users_id','release_year']).agg({'playtime_forever': 'sum'}).reset_index()
    max_user= filter_game['users_id'].iloc[0]
    
    user_playtime_by_year = user_year[user_year['users_id'] == max_user][['release_year', 'playtime_forever']]
    user_playtime_by_year.rename(columns={'release_year':'Año','playtime_forever':'Tiempo Jugado'}, inplace=True)
    year_playtime= user_playtime_by_year.to_dict('records')
    
    return {"Usuario con más horas jugadas para Género " + genre: max_user, "Horas jugadas": year_playtime}

@app.get('/best_developer_year', tags=['GET'])
def best_developer_year( año : int= Query(default= 2012)):
    
    '''Ingresa un año y te retorna la desarolladora con más reviews positivas'''
    
    game=games[['developer','app_name','id','principal_genre','release_year']]
    review=reviews[['item_id','senti_positivo']]
    game=game[game['release_year']== año]
    
    reviews_filter= game.merge(review, left_on='id', right_on='item_id', how= 'inner')
    reviews_filter= reviews_filter[['developer','app_name','senti_positivo']]
    reviews_filter=reviews_filter.groupby(['developer']).agg({'senti_positivo':'sum'}).reset_index()
    reviews_filter= reviews_filter.sort_values(by= 'senti_positivo', ascending= False)
    
    developer= list(reviews_filter.iloc[:,0])
    positive=list(reviews_filter.iloc[:,1])
   
    return [{'Top 1': [{'Developer':developer[0]},{'Reviews positive':positive[0]}]},
            {'Top 2': [{'Developer':developer[1]},{'Reviews positive':positive[1]}]},
            {'Top 3': [{'Developer':developer[2]},{'Reviews positive':positive[2]}]}]
    

@app.get('/Developer_Reviews_Analysis', tags=['GET'])
def developer_reviews_analysis( desarrolladora : str=Query(default='Bethesda Game Studios') ):
    
    '''Ingresa una desarrolladora y te retorna la cantidad de reviews positivas y negativas que tiene'''
    
    game= games[['id','developer']]
    review= reviews[['item_id', 'senti_negativo','senti_positivo']]
    game= game[game['developer']== desarrolladora]
    game_filter= game.merge(review, left_on='id', right_on='item_id', how='inner')
    game_filter= game_filter.groupby('developer').agg({'senti_negativo':'sum',
                                                       'senti_positivo':'sum'}).reset_index()
    developer= game_filter['developer'].iloc[0]
    review_neg= game_filter['senti_negativo'].iloc[0]
    review_pos= game_filter['senti_positivo'].iloc[0]
    return {developer:[{'Positivas': review_pos},{'Negativas':review_neg}]}

@app.get('/Recomendacion Juego', tags=['Recomendacion'])
def recomendacion_juego(id_de_producto: int= Query(default=413120)):
    
    '''Ingresa un ID de un juego y retorna una lista de juegos similares que te pueden interesar 
    usan un modelo de similitud del coseno'''

    atributos = games[games['id'] == id_de_producto]
    
    if atributos.empty:
        return 'No se encontró un juego con el ID proporcionado, prueba otro ID.'
    
    juegos = games[games['principal_genre'] == atributos['principal_genre'].iloc[0]]
    juegos= juegos[['app_name','principal_genre','principal_tag','principal_spec']]
    juegos['caracteristicas'] = juegos[['principal_genre', 'principal_tag', 'principal_spec']].apply(lambda row: '-'.join(row.values.astype(str)), axis=1) 
    juegos= juegos[['app_name','caracteristicas']].iloc[:1001,:]
    
    vector= TfidfVectorizer()
    matriz= vector.fit_transform(juegos['caracteristicas'])
    matriz_similaridad= cosine_similarity(matriz)
    
    indice_juego = juegos.index[juegos['app_name'] == atributos['app_name'].iloc[0]].tolist()[0]
    similares = list(enumerate(matriz_similaridad[indice_juego]))
    similaridades = sorted(similares, key=lambda x: x[1], reverse=True)[1:6]
    juegos_recomendados = [juegos.iloc[i[0]]['app_name'] for i in similaridades]
    
    return {'Juegos similares que te pueden interesar': juegos_recomendados}

@app.get('/Recomendacion Juego por usuario', tags=['Recomendacion'])
def recomendacion_usuario( id_de_usuario: str=Query('doctr')):
    
    '''Ingresa un ID de un usuario y retorna una lista de juegos similares que le pueden interesar 
    usan un modelo de similitud del coseno'''
    
    items[['item_id','users_id']]
    items[['item_id','users_id']] 
    item= items[items['users_id']==id_de_usuario]
    ids= item['item_id']
    item= item.merge(games, left_on='item_id', right_on='id', how= 'inner')
    item= item[['principal_genre','item_id']]
    
    genre= pd.DataFrame(item['principal_genre'].value_counts())[:2]
    genre= genre.index.tolist()
    
    game= games[games['principal_genre'].isin(genre)][['app_name','id','principal_genre','principal_tag','principal_spec']] 
    game= game[~game['id'].isin(ids.tolist())].iloc[:1001,:]
    game['caracteristicas']= game[['principal_genre', 'principal_tag', 'principal_spec']].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
    game=game[['app_name','id','caracteristicas']]
    
    vector= TfidfVectorizer()
    matriz= vector.fit_transform(game['caracteristicas'])
    matriz_similaridad= cosine_similarity(matriz)
    similares = list(enumerate(matriz_similaridad))
    similaridades = sorted(similares, key=lambda x: x[0], reverse=True)[1:6]
    juegos_recomendados = [game.iloc[i[0]]['app_name'] for i in similaridades]
    
    return {'Juegos similares que te pueden interesar a ti '+ id_de_usuario: juegos_recomendados}