# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:43:13 2025

@author: pablo
"""

import pandas as pd

# Leer el archivo
df = pd.read_csv('muon_hits_complete.csv')

# Contar hits para TODOS los eventos (0 hits incluidos)
hits_por_evento = df.groupby('Evento').apply(
    lambda grupo: (grupo[['X', 'Y', 'Z']] != -99999).all(axis=1).sum()
)

# hits_por_evento es una Series de pandas donde:
# - El índice es el número de evento (0, 1, 2, ...)
# - Los valores son el conteo de hits (ej: 2 para el evento 0)

print(hits_por_evento[0])
