# 📊 Sistema de Automatización y Detección de Anomalías en Gastos de Viáticos

Solución automatizada en Python para el análisis estadístico, detección de atípicos (*outliers*) y generación de visualizaciones ejecutivas sobre reportes de gastos operativos.

---

## 🎯 Caso de Uso
Automatización del proceso de revisión de gastos semanales para un equipo comercial de ventas. Reemplaza el procesamiento manual en hojas de cálculo por un pipeline modular que consolida datos, calcula métricas clave y genera alertas de auditoría visuales en segundos.

---

## 🏗️ Arquitectura del Proyecto

```text
gastos_proyecto/
│
├── config/
│   └── app_config.yaml      # Configuración de negocio e inyección de parámetros
├── src/
│   ├── __init__.py
│   ├── database.py          # Extracción, generación y estructuración de datos
│   └── logic.py             # Motor estadístico, detección de atípicos y gráficos
│
├── .gitignore               # Archivos excluidos del control de versiones
├── dashboard_viaticos.png   # Dashboard ejecutivo generado
├── main.py                  # Orquestador principal de la aplicación
└── requirements.txt         # Dependencias del proyecto