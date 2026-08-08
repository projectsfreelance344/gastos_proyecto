import random
from datetime import datetime, timedelta

def generar_datos_ficticios(config):
    random.seed(42)
    empleados = config["empleados"]
    rangos = config["rangos_normales"]
    fecha_inicio = datetime.strptime(config["reporte"]["semana_inicio"], "%Y-%m-%d")
    
    categorias = list(rangos.keys())
    registros = []

    for _ in range(60):
        emp = random.choice(empleados)
        cat = random.choice(categorias)
        min_monto, max_monto = rangos[cat]
        monto = round(random.uniform(min_monto, max_monto), 2)
        fecha = fecha_inicio + timedelta(days=random.randint(0, 6))
        
        registros.append({
            "empleado": emp,
            "categoria": cat,
            "monto": monto,
            "fecha": fecha.strftime("%Y-%m-%d")
        })

    # Inyección de gastos atípicos simulados
    registros.extend([
        {"empleado": "Diego Cortés", "categoria": "Hospedaje", "monto": 4800.00, "fecha": "2025-11-05"},
        {"empleado": "Karla Díaz", "categoria": "Representacion", "monto": 3200.00, "fecha": "2025-11-06"},
        {"empleado": "Luis Ramírez", "categoria": "Transporte", "monto": 1850.00, "fecha": "2025-11-07"}
    ])
    
    return registros