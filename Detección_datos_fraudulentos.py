#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de auditoría de datos de campo: Detección de anomalías en mediciones.
Asignatura: Proyectos de Ingeniería Civil.

Método: Análisis de distribución del último dígito (Terminal Digit Analysis).
Utiliza el test estadístico de bondad de ajuste Chi-cuadrado para comprobar la 
uniformidad del último dígito. Si la distribución difiere significativamente 
de la uniforme, existe una alta probabilidad de manipulación humana (datos inventados).
"""

def extraer_ultimo_digito(numero):
    """
    Convierte la medición a texto y extrae el último carácter numérico.
    Se asume que todas las mediciones tienen la misma precisión decimal (ej. 98.5).
    """
    str_num = str(numero).strip()
    return int(str_num[-1])

def auditoria_chi_cuadrado(mediciones, nombre_lote="Lote de Ensayo"):
    """
    Realiza el test Chi-cuadrado sobre una lista de resultados de laboratorio o campo.
    """
    n_total = len(mediciones)
    
    if n_total < 20:
        print(f"\n--- {nombre_lote} ---")
        print("Advertencia: Se necesitan más datos (mínimo 20) para un análisis estadístico fiable.")
        return
        
    # Inicializamos el contador de frecuencias para los dígitos del 0 al 9
    frecuencias = {i: 0 for i in range(10)}
    
    for med in mediciones:
        ultimo = extraer_ultimo_digito(med)
        frecuencias[ultimo] += 1
        
    # En una distribución natural, cada dígito debería aparecer el 10% de las veces
    frecuencia_esperada = n_total / 10.0
    
    # Cálculo del estadístico Chi-cuadrado
    chi_cuadrado = 0.0
    for digito, frec_observada in frecuencias.items():
        chi_cuadrado += ((frec_observada - frecuencia_esperada) ** 2) / frecuencia_esperada
        
    # Valor crítico de Chi-cuadrado para 9 grados de libertad (dígitos 0-9) 
    # y un nivel de confianza del 95% (alpha = 0.05).
    VALOR_CRITICO = 16.919 
    
    # Impresión del informe
    print(f"\n--- INFORME DE AUDITORÍA: {nombre_lote} ---")
    print(f"Total de mediciones analizadas: {n_total}")
    
    print("Frecuencia de aparición del último dígito:")
    for d in range(10):
        print(f"Dígito {d}: {frecuencias[d]} veces (Esperado: {frecuencia_esperada:.1f})")
        
    print("-" * 45)
    print(f"Estadístico Chi-cuadrado obtenido: {chi_cuadrado:.3f}")
    print(f"Valor crítico de rechazo (95%):    {VALOR_CRITICO:.3f}")
    
    if chi_cuadrado > VALOR_CRITICO:
        print(">> RESULTADO: SOSPECHOSO.")
        print(">> La distribución no es uniforme. Alta probabilidad de intervención humana")
        print(">> (datos de campo inventados o sesgo severo en la lectura del equipo).")
    else:
        print(">> RESULTADO: NATURAL.")
        print(">> Los datos se ajustan a la variabilidad estadística esperada en obra.")

if __name__ == "__main__":
    # CASO 1: Datos de densidad de campo INVENTADOS por un operario.
    # El cerebro humano tiende a evitar el 0 y el 5 para que "no parezca inventado",
    # y suele abusar de números impares como el 3 o el 7.
    datos_inventados = [
        98.3, 99.1, 97.7, 100.2, 98.8, 99.3, 97.4, 98.7, 99.2, 98.3,
        100.1, 97.9, 98.3, 99.7, 98.4, 99.1, 97.3, 98.7, 99.9, 98.2,
        99.3, 97.7, 98.1, 100.3, 98.7, 99.3, 97.1, 98.4, 99.7, 98.3
    ]
    
    # CASO 2: Datos REALES de densidades in situ.
    # El último decimal es fruto de la variabilidad del terreno y del equipo nuclear,
    # distribuyéndose de forma prácticamente aleatoria.
    datos_naturales = [
        98.5, 99.1, 97.0, 100.6, 98.2, 99.8, 97.4, 98.9, 99.3, 98.7,
        100.0, 97.5, 98.1, 99.6, 98.4, 99.2, 97.8, 98.3, 99.9, 98.0,
        99.5, 97.2, 98.6, 100.1, 98.8, 99.4, 97.7, 98.5, 99.0, 98.3
    ]
    
    auditoria_chi_cuadrado(datos_inventados, nombre_lote="Terraplén PK 1+200 (Sospechoso)")
    auditoria_chi_cuadrado(datos_naturales, nombre_lote="Terraplén PK 1+400 (Real)")