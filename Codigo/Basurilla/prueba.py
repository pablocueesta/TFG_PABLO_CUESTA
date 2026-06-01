# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:43:13 2025

@author: pablo
"""

import pandas as pd
import numpy as np

# Leer el archivo
archivo=r"C:\Users\pablo\OneDrive\Escritorio\FISICA\Cuarto Fisica\TFG\muon_hits_complete.csv"
df = pd.read_csv(archivo)
primeros_12_eventos = df[df['Evento'] < 12]  # Asumiendo que los eventos son 0,1,2,...,12

# Contar hits para los primeros 12 eventos (0 hits incluidos)
hits_por_evento = primeros_12_eventos.groupby('Evento').apply(
    lambda grupo: (grupo[['X', 'Y', 'Z']] != -99999).all(axis=1).sum()
)

print(hits_por_evento.head(12))  # Muestra los primeros 12 eventos

# Función para calcular ResX y ResY
def calcular_residuos(evento_id, datos_evento):
    # Filtrar hits válidos (X, Y, Z != -99999)
    hits_validos = datos_evento[datos_evento[['X', 'Y', 'Z']].ne(-99999).all(axis=1)]
    detectores_activos = hits_validos['Detector'].tolist()
    
    # Caso 1: Detectores 0, 1, 2 activos
    if set(detectores_activos) == {0, 1, 2}:
        x0, z0 = hits_validos[hits_validos['Detector'] == 0][['X', 'Z']].values[0]
        x2, z2 = hits_validos[hits_validos['Detector'] == 2][['X', 'Z']].values[0]
        x1_real, z1 = hits_validos[hits_validos['Detector'] == 1][['X', 'Z']].values[0]
        
        # Calcular x1_teórico
        m = (x0 - x2) / (z0 - z2)
        n = x0 - m * z0
        x1_teorico = m * z1 + n
        ResX = np.abs(x1_real - x1_teorico)
        
        # Calcular ResY (análogo con Y-Z)
        y0 = hits_validos[hits_validos['Detector'] == 0]['Y'].values[0]
        y2 = hits_validos[hits_validos['Detector'] == 2]['Y'].values[0]
        y1_real = hits_validos[hits_validos['Detector'] == 1]['Y'].values[0]
        m_y = (y0 - y2) / (z0 - z2)
        n_y = y0 - m_y * z0
        y1_teorico = m_y * z1 + n_y
        ResY = np.abs(y1_real - y1_teorico)
    
    # Caso 2: Detectores 1, 2, 3 activos
    elif set(detectores_activos) == {1, 2, 3}:
        x1, z1 = hits_validos[hits_validos['Detector'] == 1][['X', 'Z']].values[0]
        x3, z3 = hits_validos[hits_validos['Detector'] == 3][['X', 'Z']].values[0]
        x2_real, z2 = hits_validos[hits_validos['Detector'] == 2][['X', 'Z']].values[0]
        
        # Calcular x2_teórico
        m = (x1 - x3) / (z1 - z3)
        n = x1 - m * z1
        x2_teorico = m * z2 + n
        ResX = np.abs(x2_real - x2_teorico)
        
        # Calcular ResY (análogo con Y-Z)
        y1 = hits_validos[hits_validos['Detector'] == 1]['Y'].values[0]
        y3 = hits_validos[hits_validos['Detector'] == 3]['Y'].values[0]
        y2_real = hits_validos[hits_validos['Detector'] == 2]['Y'].values[0]
        m_y = (y1 - y3) / (z1 - z3)
        n_y = y1 - m_y * z1
        y2_teorico = m_y * z2 + n_y
        ResY = np.abs(y2_real - y2_teorico)
    
    else:
        raise ValueError(f"Combinación de detectores no soportada: {detectores_activos}")
    
    return ResX, ResY

# Aplicar a eventos con 3 hits
for evento, num_hits in hits_por_evento.items():
    if num_hits == 3:
        datos_evento = primeros_12_eventos[primeros_12_eventos['Evento'] == evento]
        ResX, ResY = calcular_residuos(evento, datos_evento)
        print(f"Evento {evento}: ResX = {ResX:.2f}, ResY = {ResY:.2f}")
        
def calcular_residuos_4hits(evento_id, datos_evento):
    # Obtener todos los hits válidos del evento (4 en este caso)
    hits_validos = datos_evento[datos_evento[['X', 'Y', 'Z']].ne(-99999).all(axis=1)]
    detectores_activos = hits_validos['Detector'].tolist()
    
    # Verificar que hay 4 hits
    if len(detectores_activos) != 4:
        raise ValueError(f"Evento {evento_id} no tiene 4 hits detectados.")
    
    # Todas las combinaciones posibles de 3 detectores
    combinaciones = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]
    
    res_x_list = []
    res_y_list = []
    
    for combo in combinaciones:
        # Filtrar datos para la combinación actual (3 detectores)
        datos_combo = hits_validos[hits_validos['Detector'].isin(combo)]
        
        # Calcular ResX y ResY para esta combinación (usando la función de 3 hits)
        ResX, ResY = calcular_residuos(evento_id, datos_combo)
        res_x_list.append(ResX)
        res_y_list.append(ResY)
    
    # Seleccionar el mínimo ResX y ResY (pueden venir de combinaciones distintas)
    min_ResX = min(res_x_list)
    min_ResY = min(res_y_list)
    
    return min_ResX, min_ResY

# Añadir esto al bucle principal (para eventos con 4 hits)
for evento, num_hits in hits_por_evento.items():
    if num_hits == 4:
        datos_evento = primeros_12_eventos[primeros_12_eventos['Evento'] == evento]
        ResX, ResY = calcular_residuos_4hits(evento, datos_evento)
        print(f"Evento {evento}: ResX_min = {ResX:.2f}, ResY_min = {ResY:.2f}")