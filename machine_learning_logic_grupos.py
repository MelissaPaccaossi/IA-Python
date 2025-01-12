# machine_learning_logic_grupos.py

from flask import jsonify
import pandas as pd
import numpy as np

def machine_learning_logic_grupos(usuario_en, preferencias_usuario):
    # Cargar los datos
    gruposcopia = pd.read_csv('grupos.csv')

    # Dividir las etiquetas en listas
    gruposcopia['etiquetas'] = gruposcopia['etiquetas'].str.split('|')

    # Crear una copia del DataFrame para la codificación
    grupos_co = gruposcopia.copy()

    # Realizar el one-hot encoding de las etiquetas
    for index, row in gruposcopia.iterrows():
        for etiqueta in row['etiquetas']:
            grupos_co.at[index, etiqueta] = 1

    # Llenar los valores NaN con 0
    grupos_co = grupos_co.fillna(0)

    # Si no hay historial de usuario, usar las preferencias
    if not usuario_en:
        preferencias_codificadas = pd.DataFrame(columns=grupos_co.columns[3:], index=[0])
        for etiqueta in preferencias_usuario.values():
            if etiqueta in preferencias_codificadas.columns:
                preferencias_codificadas.at[0, etiqueta] = 1
        preferencias_codificadas = preferencias_codificadas.fillna(0)

        # Calcular la similaridad
        grupos_codificados = grupos_co.drop(['grupoID', 'nombre', 'etiquetas'], axis=1)
        similaridad = grupos_codificados.dot(preferencias_codificadas.transpose()).sum(axis=1)

        # Añadir la similaridad al DataFrame original
        gruposcopia['similaridad'] = similaridad

        # Ordenar por similaridad y obtener los mejores resultados
        recomendaciones = gruposcopia.sort_values(by='similaridad', ascending=False).head(5)

        recomendaciones_dict = recomendaciones[['grupoID', 'nombre', 'etiquetas', 'similaridad']].to_dict(orient='records')
        return jsonify(recomendaciones_dict)

    # Si hay historial de usuario, utilizar el enfoque basado en el historial
    else:
        gruposcopia = pd.read_csv('grupos.csv')

        gruposcopia['etiquetas'] = gruposcopia.etiquetas.str.split('|')

        grupos_co = gruposcopia.copy()
        for index, row in gruposcopia.iterrows():
            for etiquetas in row['etiquetas']:
                grupos_co.at[index,etiquetas] = 1

        grupos_co = grupos_co.fillna(0)

        print('Grupos codificadas: \n', grupos_co)

        entrada_grupos = pd.DataFrame(usuario_en)
        print('Grupos Usuario: \n', entrada_grupos)

        Id = gruposcopia[gruposcopia['nombre'].isin(entrada_grupos['nombre'].tolist())]
        entrada_grupos = pd.merge(Id, entrada_grupos)

        grupos_usuario = grupos_co[grupos_co['grupoID'].isin(entrada_grupos['grupoID'].tolist())]
        print('Grupos Usuario Codificados: \n', grupos_usuario)

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
    preferencias_usuario = {
        "destino": "Patagonia",
        "alojamiento": "hotel",
        "rango_edad": "joven",
        "genero": "femenino"
    }
    usuario_en = []
    print(machine_learning_logic_grupos(usuario_en, preferencias_usuario))


def machine_learning_add_grupo(nuevo_grupo):
    # Cargar el archivo CSV existente
    try:
        gruposcopia = pd.read_csv('grupos.csv')
    except FileNotFoundError:
        return jsonify({"error": "El archivo grupos.csv no se encuentra"})

    # Calcular el nuevo grupoID
    nuevo_grupo_id = gruposcopia["grupoID"].max() + 1 if not gruposcopia.empty else 1

    # Crear un nuevo DataFrame con el grupo a agregar
    nuevo_grupo_df = pd.DataFrame([{
        "grupoID": nuevo_grupo_id,
        # Concatenar nombre con el ID, asegurando que ambos sean cadenas
        "nombre": f"{nuevo_grupo['nombre']} {str(nuevo_grupo_id)}",
        "etiquetas": "|".join([
            nuevo_grupo["origen"],
            nuevo_grupo["destino"],
            nuevo_grupo["hospedaje"],
            nuevo_grupo["cantidad_personas"],
            nuevo_grupo["region"],
            nuevo_grupo["rango_edad"],
            nuevo_grupo["preferencia_sexo"]
        ])
    }])

    # Concatenar el nuevo grupo al DataFrame original
    gruposcopia = pd.concat([gruposcopia, nuevo_grupo_df], ignore_index=True)

    # Guardar el DataFrame actualizado en el CSV
    try:
        gruposcopia.to_csv('grupos.csv', index=False)
    except Exception as e:
        return jsonify({"error": f"Error al guardar el archivo CSV: {str(e)}"})

    return jsonify("Se agregó correctamente el grupo a la base del conocimiento")

