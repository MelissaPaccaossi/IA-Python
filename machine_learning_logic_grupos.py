# machine_learning_logic.py

from flask import jsonify
import pandas as pd

def machine_learning_logic_grupos(usuario_en):
    #importamos librerias
    import pandas as pd
    from math import sqrt #importaremos la funcion sqrt para la libreria math
    import numpy as np
    import matplotlib.pyplot as plt

    print('hola')

    peliculas = pd.read_csv('movies.csv')
    rating = pd.read_csv('rating.csv')
    grupos = pd.read_csv('grupos.csv')
    gruposcopia = pd.read_csv('gruposCopy.csv')


    print('Grupos: \n',grupos.head())
    print('Rating: \n',rating.head())

    gruposcopia['etiquetas'] = gruposcopia.etiquetas.str.split('|')

    grupos_co = gruposcopia.copy()
    for index, row in gruposcopia.iterrows():
        for etiquetas in row['etiquetas']:
            grupos_co.at[index,etiquetas] = 1

    grupos_co = grupos_co.fillna(0)

    print('Grupos codificadas: \n', grupos_co)

    # usuario_en = [
    #                 {'nombre':'Salta Cultural Tour','rating':3},                
    #                 {'nombre':'Bariloche Hiking Adventure','rating':5},                
    #                 {'nombre':'Viedma Birdwatching','rating':4},              
    #                 {'nombre':'Villa La Angostura Lakeside','rating':5},           
    #                 {'nombre':'Pampa Gaucha Experience','rating':1},           
    #                 {'nombre':'Córdoba Nightlife Tour','rating':3},           
    #             ]

    entrada_grupos = pd.DataFrame(usuario_en)
    print('Grupos Usuario: \n', entrada_grupos)

    Id = gruposcopia[gruposcopia['nombre'].isin(entrada_grupos['nombre'].tolist())]
    entrada_grupos = pd.merge(Id, entrada_grupos)

    grupos_usuario = grupos_co[grupos_co['grupoID'].isin(entrada_grupos['grupoID'].tolist())]
    print('Grupos Usuario Codificados: \n', grupos_usuario)

    # grupos_usuario = grupos_usuario.reset_index(drop=True)
    # tabla_etiquetas = grupos_usuario.drop('grupoID', 1).drop('nombre', 1).drop('etiquetas',1)
    # print('Categorias que el usuario prefiere: \n', tabla_etiquetas)

    grupos_usuario = grupos_usuario.reset_index(drop=True)
    columnas_a_eliminar = ['grupoID', 'nombre', 'etiquetas']
    tabla_etiquetas = grupos_usuario.drop(columnas_a_eliminar, axis=1)
    print('Tabla Etiquetas: \n', tabla_etiquetas)


    perfil_usu = tabla_etiquetas.transpose().dot(entrada_grupos['rating'])
    print('Etiquetas que el usuario prefiere: \n', perfil_usu)

    etiquetas = grupos_co.set_index(grupos_co['grupoID'])

    etiquetas_a_mostrar = ['grupoID','nombre','etiquetas']
    etiquetas = etiquetas.drop(etiquetas_a_mostrar, axis=1)
    print('Etiquetas: \n', etiquetas.head())
    etiquetas.shape

    recom = ((etiquetas*perfil_usu).sum(axis=1))/(perfil_usu.sum())
    print('Recomendaciones: \n', recom.head())

    recom = recom.sort_values(ascending=False)
    print('Recomendaciones Organizadas: \n', recom.head())

    final = gruposcopia.loc[gruposcopia['grupoID'].isin(recom.head(5).keys())]
    nfinal = final[['nombre']]
    print('Nombre de grupos recomendadas: \n', nfinal)


    # Realizar un join entre las recomendaciones y la tabla de películas
    recomendaciones_organizadas = pd.DataFrame(recom, columns=['Similaridad'])
    recomendaciones_organizadas.reset_index(inplace=True)
    recomendaciones_organizadas.rename(columns={'index': 'grupoID'}, inplace=True)

    recomendaciones_con_info = pd.merge(recomendaciones_organizadas, gruposcopia, on='grupoID', how='left')

    print('Recomendaciones con información de películas: \n', recomendaciones_con_info.head())


    # Lista de títulos de películas del usuario
    nombres_usuario = [entrada['nombre'] for entrada in usuario_en]

    # Filtrar las recomendaciones para excluir las películas del usuario
    recomendaciones_filtradas = recomendaciones_con_info[~recomendaciones_con_info['nombre'].isin(nombres_usuario)]
    print('Recomendaciones sin grupos visitados por el usuario: \n', recomendaciones_filtradas.head())

    recomendaciones_dict = recomendaciones_filtradas.head().to_dict(orient='records')

    # Devuelve el diccionario como respuesta JSON
    return jsonify(recomendaciones_dict)

if __name__ == "__main__":
    machine_learning_logic_grupos()
