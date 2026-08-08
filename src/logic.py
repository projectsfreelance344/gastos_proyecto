import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def calcular_estadisticas(montos):
    return {
        "total_gastado": sum(montos),
        "numero_tickets": len(montos),
        "gasto_promedio": statistics.mean(montos),
        "gasto_mediano": statistics.median(montos),
        "desviacion_estandar": statistics.stdev(montos),
    }

def detectar_atipicos(montos, umbral_desviaciones=2):
    media = statistics.mean(montos)
    desviacion = statistics.stdev(montos)
    limite = media + umbral_desviaciones * desviacion
    return [m for m in montos if m > limite], limite

def agrupar_totales(registros, clave):
    totales = {}
    for r in registros:
        totales[r[clave]] = totales.get(r[clave], 0) + r["monto"]
    return totales

def generar_dashboard(registros, montos, umbral):
    totales_cat = agrupar_totales(registros, "categoria")
    totales_emp = agrupar_totales(registros, "empleado")
    atipicos, limite = detectar_atipicos(montos, umbral)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Reporte Semanal de Gastos de Viáticos — Equipo de Ventas", fontsize=14, fontweight="bold")

    # 1. Gasto por categoría
    cats, vals = list(totales_cat.keys()), list(totales_cat.values())
    barras = axes[0, 0].bar(cats, vals, color="#4C72B0", edgecolor="black")
    axes[0, 0].set_title("Gasto total por categoría")
    axes[0, 0].yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
    for b in barras:
        axes[0, 0].text(b.get_x() + b.get_width() / 2, b.get_height(), f"${b.get_height():,.0f}", ha="center", va="bottom", fontsize=8)

    # 2. Gasto por empleado
    emps, vals_emp = list(totales_emp.keys()), list(totales_emp.values())
    axes[0, 1].barh(emps, vals_emp, color="#DD8452", edgecolor="black")
    axes[0, 1].set_title("Gasto total por empleado")
    axes[0, 1].xaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))

    # 3. Distribución
    axes[1, 0].hist(montos, bins=15, color="#55A868", edgecolor="black", alpha=0.8)
    axes[1, 0].axvline(statistics.mean(montos), color="blue", linestyle="dashed", linewidth=2, label=f"Promedio: ${statistics.mean(montos):,.0f}")
    axes[1, 0].axvline(limite, color="red", linestyle="dashed", linewidth=2, label=f"Umbral atípico: ${limite:,.0f}")
    axes[1, 0].set_title("Distribución de montos por ticket")
    axes[1, 0].legend(fontsize=8)

    # 4. Proporción
    axes[1, 1].pie(vals, labels=cats, autopct="%1.1f%%", startangle=90, colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"])
    axes[1, 1].set_title("Proporción del gasto por categoría")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("dashboard_viaticos.png", dpi=150)
    plt.close()

    return atipicos, limite