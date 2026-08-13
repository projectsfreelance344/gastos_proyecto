import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.database import generar_datos_ficticios
from src.logic import calcular_estadisticas, generar_dashboard

console = Console()


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

    console.print(Panel.fit(
        "[bold]REPORTE EJECUTIVO — GASTOS DE VIÁTICOS[/bold]",
        border_style="blue",
    ))

    tabla_resumen = Table(show_header=True, header_style="bold cyan")
    tabla_resumen.add_column("Indicador")
    tabla_resumen.add_column("Valor", justify="right")
    tabla_resumen.add_row("Total gastado", f"${resumen['total_gastado']:,.2f}")
    tabla_resumen.add_row("Número de tickets", str(resumen["numero_tickets"]))
    tabla_resumen.add_row("Gasto promedio", f"${resumen['gasto_promedio']:,.2f}")
    tabla_resumen.add_row("Gasto mediano", f"${resumen['gasto_mediano']:,.2f}")
    tabla_resumen.add_row("Desviación estándar", f"${resumen['desviacion_estandar']:,.2f}")
    console.print(tabla_resumen)

    console.print(
        f"\n[yellow]Umbral de gasto atípico[/yellow] "
        f"({umbral_config} desv. estándar): [bold]${limite:,.2f}[/bold]"
    )

    if atipicos:
        tabla_atipicos = Table(
            title=f"Gastos atípicos detectados: {len(atipicos)}",
            show_header=True, header_style="bold red",
        )
        tabla_atipicos.add_column("Empleado")
        tabla_atipicos.add_column("Categoría")
        tabla_atipicos.add_column("Monto", justify="right")
        for monto in atipicos:
            registro = next(r for r in registros if r["monto"] == monto)
            tabla_atipicos.add_row(
                registro["empleado"], registro["categoria"], f"${monto:,.2f}"
            )
        console.print(tabla_atipicos)
    else:
        console.print("[green]No se detectaron gastos atípicos.[/green]")

    console.print(f"\n[bold green]✅ Dashboard guardado en:[/bold green] dashboard_viaticos.png")


if __name__ == "__main__":
    main()