#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de automatización de cálculo de volúmenes y costes de movimiento de tierras.
Asignatura: Proyectos de Ingeniería Civil.
"""

def calcular_volumen_areas_medias(area_perfil_1, area_perfil_2, distancia):
    """
    Calcula el volumen entre dos perfiles transversales usando el método de las áreas medias.
    """
    return ((area_perfil_1 + area_perfil_2) / 2) * distancia

def estimar_coste_movimiento_tierras(perfiles, precio_desmonte, precio_terraplen):
    """
    Calcula el coste total iterando sobre una lista de perfiles topográficos.
    
    :param perfiles: Lista de diccionarios con la distancia al origen, área de desmonte y área de terraplén.
    :param precio_desmonte: Coste unitario de excavación (€/m3).
    :param precio_terraplen: Coste unitario de relleno y compactación (€/m3).
    """
    volumen_total_desmonte = 0.0
    volumen_total_terraplen = 0.0
    coste_total = 0.0

    print("--- INFORME DE MOVIMIENTO DE TIERRAS ---")
    
    for i in range(len(perfiles) - 1):
        p1 = perfiles[i]
        p2 = perfiles[i+1]
        
        distancia_tramo = p2['pk'] - p1['pk']
        
        vol_desmonte = calcular_volumen_areas_medias(p1['area_desmonte'], p2['area_desmonte'], distancia_tramo)
        vol_terraplen = calcular_volumen_areas_medias(p1['area_terraplen'], p2['area_terraplen'], distancia_tramo)
        
        volumen_total_desmonte += vol_desmonte
        volumen_total_terraplen += vol_terraplen
        
        coste_tramo = (vol_desmonte * precio_desmonte) + (vol_terraplen * precio_terraplen)
        coste_total += coste_tramo
        
        print(f"Tramo PK {p1['pk']} a PK {p2['pk']}: Desmonte = {vol_desmonte:.2f} m3 | Terraplén = {vol_terraplen:.2f} m3")

    print("-" * 40)
    print(f"Volumen Total Desmonte: {volumen_total_desmonte:.2f} m3")
    print(f"Volumen Total Terraplén: {volumen_total_terraplen:.2f} m3")
    print(f"COSTE TOTAL ESTIMADO: {coste_total:.2f} €")
    
    return coste_total

if __name__ == "__main__":
    # Datos de ejemplo levantamiento topográfico
    datos_perfiles = [
        {'pk': 0, 'area_desmonte': 15.5, 'area_terraplen': 0.0},
        {'pk': 20, 'area_desmonte': 12.0, 'area_terraplen': 2.5},
        {'pk': 40, 'area_desmonte': 0.0, 'area_terraplen': 18.4},
        {'pk': 60, 'area_desmonte': 0.0, 'area_terraplen': 22.1}
    ]
    
    # Precios unitarios de la base de datos de la constructora
    PRECIO_M3_DESMONTE = 4.50  # €/m3
    PRECIO_M3_TERRAPLEN = 6.20 # €/m3
    
    estimar_coste_movimiento_tierras(datos_perfiles, PRECIO_M3_DESMONTE, PRECIO_M3_TERRAPLEN)