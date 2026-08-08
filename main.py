import yaml
from src.database import generar_datos_ficticios
from src.logic import calcular_estadisticas, generar_dashboard

def cargar_configuracion():
    with open("config/app_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = cargar_configuracion()
    registros = generar_datos_ficticios(config)
    montos = [r["monto"] for r in registros]
    
    umbral_config = config["reporte"]["umbral_desviaciones"]
    resumen = calcular_estadisticas(montos)
    atipicos, limite = generar_dashboard(registros, montos, umbral_config)

    print("=" * 60)
    print("REPORTE EJECUTIVO — GASTOS DE VIÁTICOS")
    print("=" * 60)
    print(f"Total gastado:         ${resumen['total_gastado']:,.2f}")
    print(f"Número de tickets:    {resumen['numero_tickets']}")
    print(f"Gasto promedio:        ${resumen['gasto_promedio']:,.2f}")
    print(f"Gasto mediano:         ${resumen['gasto_mediano']:,.2f}")
    print(f"Desviación estándar:  ${resumen['desviacion_estandar']:,.2f}")
    print("-" * 60)
    print(f"Umbral de gasto atípico ({umbral_config} desv. estándar): ${limite:,.2f}")
    print(f"Gastos atípicos detectados: {len(atipicos)}")
    for monto in atipicos:
        registro = next(r for r in registros if r["monto"] == monto)
        print(f"  → {registro['empleado']} | {registro['categoria']} | ${monto:,.2f} | {registro['fecha']}")
    print("=" * 60)
    print("Dashboard guardado en: dashboard_viaticos.png")
    print("=" * 60)

if __name__ == "__main__":
    main()