
import pandas as pd
import numpy as np

archivo = r"C:\Users\pablo\OneDrive\Escritorio\FISICA\Cuarto Fisica\TFG\muon_hits_complete.csv"
df = pd.read_csv(archivo)

primeros_12_eventos = df[df['Evento'] < 12]  # Asumiendo que los eventos son 0,1,2,...,12

# Filtrar solo eventos con exactamente 3 o 4 hits válidos (X, Y, Z != -99999)
def contar_hits_validos(grupo):
    return (grupo[['X', 'Y', 'Z']] != -99999).all(axis=1).sum()

# Agrupar por evento y contar hits válidos
hits_validos_por_evento = primeros_12_eventos.groupby('Evento').apply(contar_hits_validos)

# Seleccionar solo eventos con 3 o 4 hits válidos
eventos_filtrados = hits_validos_por_evento[(hits_validos_por_evento == 3) | (hits_validos_por_evento == 4)]

hits_por_evento = eventos_filtrados

# 3 HITS
def calcular_residuos(evento_id, datos_evento):
    hits_validos = datos_evento[datos_evento[['X', 'Y', 'Z']].ne(-99999).all(axis=1)]
    detectores_activos = sorted(hits_validos['Detector'].tolist())
    
    if len(detectores_activos) != 3:
        raise ValueError(f"Evento {evento_id}: Se esperaban 3 detectores activos.")
    
    detector_intermedio = detectores_activos[1]
    coords = {d: hits_validos[hits_validos['Detector'] == d][['X', 'Y', 'Z']].values[0] for d in detectores_activos}
    
    izquierdo, derecho = detectores_activos[0], detectores_activos[2]
    x_izq, y_izq, z_izq = coords[izquierdo]
    x_der, y_der, z_der = coords[derecho]
    x_real, y_real, z_intermedio = coords[detector_intermedio]
    
    m_x = (x_izq - x_der) / (z_izq - z_der)
    x_teorico = m_x * z_intermedio + (x_izq - m_x * z_izq)
    ResX = np.abs(x_real - x_teorico)
    
    m_y = (y_izq - y_der) / (z_izq - z_der)
    y_teorico = m_y * z_intermedio + (y_izq - m_y * z_izq)
    ResY = np.abs(y_real - y_teorico)
    
    return ResX, ResY

# 4 HITS
def calcular_residuos_4hits(evento_id, datos_evento):
    hits_validos = datos_evento[datos_evento[['X', 'Y', 'Z']].ne(-99999).all(axis=1)]
    if len(hits_validos) != 4:
        raise ValueError(f"Evento {evento_id}: Se esperaban 4 detectores activos.")
    
    combinaciones = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]
    
    res_x_list, res_y_list = [], []
    for combo in combinaciones:
        datos_combo = hits_validos[hits_validos['Detector'].isin(combo)]
        ResX, ResY = calcular_residuos(evento_id, datos_combo)
        res_x_list.append(ResX)
        res_y_list.append(ResY)
    
    return min(res_x_list), min(res_y_list)

# BUCLE PRINCIPAL
for evento, num_hits in hits_por_evento.items():
    if num_hits == 3:
        datos_evento = df[df['Evento'] == evento]
        ResX, ResY = calcular_residuos(evento, datos_evento)
        print(f"Evento {evento}, 3 hits: ResX = {ResX:.2f}, ResY = {ResY:.2f}")
    elif num_hits == 4:
        datos_evento = df[df['Evento'] == evento]
        ResX, ResY = calcular_residuos_4hits(evento, datos_evento)
        print(f"Evento {evento}, 4 hits: ResX_min = {ResX:.2f}, ResY_min = {ResY:.2f}")
