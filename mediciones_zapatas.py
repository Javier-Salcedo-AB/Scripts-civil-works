#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para el cálculo automático de mediciones en cimentaciones superficiales (zapatas aisladas).
Asignatura: Proyectos de Ingeniería Civil.
"""

class Zapata:
    def __init__(self, identificador, longitud, anchura, canto, cuantia_acero):
        self.id = identificador
        self.L = longitud        # metros
        self.B = anchura         # metros
        self.H = canto           # metros
        self.cuantia = cuantia_acero # kg/m3

    def calcular_volumen_hormigon(self):
        return self.L * self.B * self.H

    def calcular_superficie_encofrado(self):
        # Solo se encofran las caras laterales
        return 2 * (self.L * self.H) + 2 * (self.B * self.H)

    def calcular_kilos_acero(self):
        return self.calcular_volumen_hormigon() * self.cuantia

def generar_resumen_mediciones(lista_zapatas):
    """
    Agrega las mediciones de una lista de objetos Zapata y genera el resumen para certificación.
    """
    total_hormigon = 0.0
    total_encofrado = 0.0
    total_acero = 0.0
    
    print(f"{'ID Zapata':<12} | {'Hormigón (m3)':<15} | {'Encofrado (m2)':<15} | {'Acero (kg)':<12}")
    print("-" * 65)

    for zapata in lista_zapatas:
        v_hormigon = zapata.calcular_volumen_hormigon()
        s_encofrado = zapata.calcular_superficie_encofrado()
        k_acero = zapata.calcular_kilos_acero()
        
        total_hormigon += v_hormigon
        total_encofrado += s_encofrado
        total_acero += k_acero
        
        print(f"{zapata.id:<12} | {v_hormigon:<15.2f} | {s_encofrado:<15.2f} | {k_acero:<12.2f}")
        
    print("-" * 65)
    print("TOTALES DE OBRA:")
    print(f"- HA-25/B/20/IIa: {total_hormigon:.2f} m3")
    print(f"- Encofrado de madera: {total_encofrado:.2f} m2")
    print(f"- Acero B-500-S: {total_acero:.2f} kg")

if __name__ == "__main__":
    # Base de datos de elementos de cimentación extraídos del modelo
    zapatas_proyecto = [
        Zapata("Z-01", 2.0, 2.0, 0.8, 55.0),
        Zapata("Z-02", 2.0, 2.0, 0.8, 55.0),
        Zapata("Z-03", 2.5, 2.5, 1.0, 60.0),
        Zapata("Z-04", 3.0, 2.5, 1.0, 65.0)
    ]
    
    generar_resumen_mediciones(zapatas_proyecto)