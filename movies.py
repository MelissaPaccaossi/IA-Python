#importamos librerias
import pandas as pd
from math import sqrt #importaremos la funcion sqrt para la libreria math
import numpy as np
import matplotlib.pyplot as plt

print('hola')

peliculas = pd.read_csv('movies.csv')

print('Peliculas: \n',peliculas.head())