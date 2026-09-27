# 🏗️ Automatización en Proyectos de Ingeniería Civil

Repositorio educativo *open-source* con herramientas de programación y automatización aplicadas a la gestión y control de proyectos de construcción civil. 

Este material forma parte de la asignatura de **Proyectos de Ingeniería Civil** en la **Universidad Politécnica de Madrid (UPM)**, diseñado para cubrir la brecha existente en ejemplos prácticos de programación para ingenieros civiles.

## 📦 Scripts Disponibles

1. **`movimiento_tierras.py`**: Estimación de costes para movimiento de tierras (desmonte y terraplén) utilizando el método topográfico de las áreas medias.
2. **`mediciones_zapatas.py`**: Extracción y resumen automatizado de mediciones (volumen de hormigón, superficie de encofrado y kilos de acero) mediante Programación Orientada a Objetos.
3. **`auditoria_datos_campo.py`**: Detección de anomalías y posible manipulación en partes de obra (ej. densidades de compactación) mediante el test estadístico Chi-cuadrado (Ley de Benford adaptada al último dígito).

## 🚀 Instalación y Uso

Para ejecutar los scripts que procesan archivos Excel o CSV, necesitas tener instaladas las librerías estándar de análisis de datos en Python.

Abre tu terminal y ejecuta:
```bash
pip install pandas openpyxl
Para ejecutar cualquier script, navega hasta la carpeta del proyecto y usa:
Bash

python nombre_del_script.py

🤝 Contribuciones

Se anima a los estudiantes a clonar este repositorio, modificar las variables de los scripts con datos reales de obra y proponer mejoras mediante Pull Requests.