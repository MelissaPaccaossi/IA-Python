#importamos librerias
import pandas as pd
from math import sqrt #importaremos la funcion sqrt para la libreria math
import numpy as np
import matplotlib.pyplot as plt

print('hola')

peliculas = pd.read_csv('movies.csv')
rating = pd.read_csv('rating.csv')

print('Peliculas: \n',peliculas.head())
print('Rating: \n',rating.head())

peliculas['Genero'] = peliculas.Genero.str.split('|')

peliculas_co = peliculas.copy()
for index, row in peliculas.iterrows():
    for Genero in row['Genero']:
        peliculas_co.at[index,Genero] = 1

peliculas_co = peliculas_co.fillna(0)

print('Peliculas codificadas: \n', peliculas_co)

usuario_en = [
                {'Titulo':'El Padrino','rating':5},                
                {'Titulo':'Los Increíbles','rating':2},                
                {'Titulo':'El Caballero de la Noche','rating':1},
            ]

entrada_peli = pd.DataFrame(usuario_en)
print('Peliculas Usuario: \n', entrada_peli)

Id = peliculas[peliculas['Titulo'].isin(entrada_peli['Titulo'].tolist())]
entrada_peli = pd.merge(Id, entrada_peli)

peli_usuario = peliculas_co[peliculas_co['ID'].isin(entrada_peli['ID'].tolist())]
print('Peliculas Usuario Codificadas: \n', peli_usuario)

# peli_usuario = peli_usuario.reset_index(drop=True)
# tabla_generos = peli_usuario.drop('ID', 1).drop('Titulo', 1).drop('Genero',1)
# print('Categorias que el usuario prefiere: \n', tabla_generos)

peli_usuario = peli_usuario.reset_index(drop=True)
columnas_a_eliminar = ['ID', 'Titulo', 'Genero']
tabla_generos = peli_usuario.drop(columnas_a_eliminar, axis=1)
print('Tabla Generos: \n', tabla_generos)


perfil_usu = tabla_generos.transpose().dot(entrada_peli['rating'])
print('Categorias que el usuario prefiere: \n', perfil_usu)

generos = peliculas_co.set_index(peliculas_co['ID'])

generos_a_mostrar = ['ID','Titulo','Genero']
generos = generos.drop(generos_a_mostrar, axis=1)
print('Generos: \n', generos.head())
generos.shape

recom = ((generos*perfil_usu).sum(axis=1))/(perfil_usu.sum())
print('Recomendaciones: \n', recom.head())

recom = recom.sort_values(ascending=False)
print('Recomendaciones Organizadas: \n', recom.head())

final = peliculas.loc[peliculas['ID'].isin(recom.head(5).keys())]
nfinal = final[['Titulo']]
print('Nombre de peliculas recomendadas: \n', nfinal)


# Realizar un join entre las recomendaciones y la tabla de películas
recomendaciones_organizadas = pd.DataFrame(recom, columns=['Similaridad'])
recomendaciones_organizadas.reset_index(inplace=True)
recomendaciones_organizadas.rename(columns={'index': 'ID'}, inplace=True)

recomendaciones_con_info = pd.merge(recomendaciones_organizadas, peliculas, on='ID', how='left')

print('Recomendaciones con información de películas: \n', recomendaciones_con_info.head())


# Lista de títulos de películas del usuario
titulos_usuario = [entrada['Titulo'] for entrada in usuario_en]

# Filtrar las recomendaciones para excluir las películas del usuario
recomendaciones_filtradas = recomendaciones_con_info[~recomendaciones_con_info['Titulo'].isin(titulos_usuario)]

print('Recomendaciones sin películas del usuario: \n', recomendaciones_filtradas.head())




