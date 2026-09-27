#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de auditoría de datos de campo mediante importación masiva (CSV/Excel).
Asignatura: Proyectos de Ingeniería Civil.

Este script amplía el análisis estadístico de último dígito (Chi-cuadrado) para 
procesar grandes volúmenes de datos exportados desde equipos de compactación, 
prensa de rotura de probetas o registros topográficos.
"""

import pandas as pd
import os

def extraer_ultimo_digito(numero):
    """
    Extrae el último dígito numérico de un valor.
    Se han añadido filtros para evitar errores con celdas vacías (NaN) o textos en el Excel.
    """
    if pd.isna(numero):
        return None
        
    str_num = str(numero).strip()
    
    # Nos aseguramos de coger el último carácter numérico, descartando posibles 
    # unidades de medida escritas en la celda por error (ej. "98.5 %")
    for char in reversed(str_num):
        if char.isdigit():
            return int(char)
            
    return None

def auditoria_chi_cuadrado(mediciones, nombre_lote="Lote de Ensayo"):
    """
    Realiza el test Chi-cuadrado sobre una lista/serie de datos filtrada.
    """
    # Filtramos valores nulos que hayan podido llegar hasta aquí
    mediciones_validas = [m for m in mediciones if m is not None]
    n_total = len(mediciones_validas)
    
    if n_total < 20:
        print(f"\n--- {nombre_lote} ---")
        print(f"Advertencia: Solo hay {n_total} datos válidos.")
        print("Se necesitan más datos (mínimo 20) para un análisis estadístico fiable.")
        return
        
    frecuencias = {i: 0 for i in range(10)}
    
    for med in mediciones_validas:
        ultimo = extraer_ultimo_digito(med)
        if ultimo is not None:
            frecuencias[ultimo] += 1
            
    frecuencia_esperada = n_total / 10.0
    
    chi_cuadrado = sum(((frec_observada - frecuencia_esperada) ** 2) / frecuencia_esperada 
                       for frec_observada in frecuencias.values())
        
    VALOR_CRITICO = 16.919 # Para alpha = 0.05 y 9 grados de libertad
    
    print(f"\n--- INFORME DE AUDITORÍA: {nombre_lote} ---")
    print(f"Total de mediciones analizadas: {n_total}")
    print(f"Estadístico Chi-cuadrado obtenido: {chi_cuadrado:.3f}")
    
    if chi_cuadrado > VALOR_CRITICO:
        print(">> RESULTADO: SOSPECHOSO. Distribución no uniforme (Posible manipulación).")
    else:
        print(">> RESULTADO: NATURAL. Datos conformes a la variabilidad esperada.")

def analizar_archivo_datos(ruta_archivo, nombre_columna):
    """
    Lee un archivo CSV o Excel, extrae la columna indicada y lanza la auditoría.
    """
    print(f"\nCargando datos desde: {ruta_archivo}")
    try:
        # Detectamos la extensión para usar el motor de pandas adecuado
        if ruta_archivo.endswith('.csv'):
            df = pd.read_csv(ruta_archivo, sep=None, engine='python')
        elif ruta_archivo.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(ruta_archivo)
        else:
            print("Formato no soportado. Usa .csv o .xlsx")
            return
            
        if nombre_columna not in df.columns:
            print(f"Error: La columna '{nombre_columna}' no existe en el archivo.")
            print(f"Columnas disponibles: {list(df.columns)}")
            return
            
        # Extraemos los datos de la columna como lista
        datos_crudos = df[nombre_columna].tolist()
        
        auditoria_chi_cuadrado(datos_crudos, nombre_lote=f"Archivo {os.path.basename(ruta_archivo)}")
        
    except FileNotFoundError:
        print(f"Error: No se ha encontrado el archivo {ruta_archivo}")
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")

def _generar_csv_prueba():
    """
    Función auxiliar de uso docente. Genera un CSV de prueba en la misma carpeta 
    para que los alumnos puedan testear el script inmediatamente.
    """
    nombre_archivo = "registro_densidades_obra.csv"
    if not os.path.exists(nombre_archivo):
        print(f"Generando archivo de prueba '{nombre_archivo}' para la primera ejecución...")
        
        # Mezcla de datos para simular un archivo real (unos naturales, otros alterados)
        datos_mock = {
            'ID_Ensayo': [f"ENS-{i:03d}" for i in range(1, 51)],
            'Densidad_In_Situ': [
                98.3, 99.1, 97.7, 100.2, 98.8, 99.3, 97.4, 98.7, 99.2, 98.3,
                100.1, 97.9, 98.3, 99.7, 98.4, 99.1, 97.3, 98.7, 99.9, 98.2,
                99.3, 97.7, 98.1, 100.3, 98.7, 99.3, 97.1, 98.4, 99.7, 98.3,
                98.5, 99.1, 97.0, 100.6, 98.2, 99.8, 97.4, 98.9, 99.3, 98.7,
                100.0, 97.5, 98.1, 99.6, 98.4, 99.2, 97.8, 98.3, 99.9, 98.0
            ],
            'Operario': ['Carlos'] * 30 + ['Laura'] * 20
        }
        
        df_mock = pd.DataFrame(datos_mock)
        df_mock.to_csv(nombre_archivo, index=False)

if __name__ == "__main__":
    # 1. Aseguramos que existe el archivo de prueba (solo fines educativos)
    _generar_csv_prueba()
    
    # 2. Llamada a la función de análisis
    # Para usarlo con otro archivo, basta con cambiar la ruta y el nombre de la columna.
    ARCHIVO_A_ANALIZAR = "registro_densidades_obra.csv"
    COLUMNA_OBJETIVO = "Densidad_In_Situ"
    
    analizar_archivo_datos(ARCHIVO_A_ANALIZAR, COLUMNA_OBJETIVO)