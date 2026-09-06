"""
Calculadora de Préstamo Hipotecario (versión de consola)
---------------------------------------------------------
Calcula cuánto ahorras en intereses y cuánto reduces el plazo de tu
préstamo hipotecario al hacer un abono extra a capital.

Datos solicitados al usuario:
  1. Tasa actual del préstamo (anual, en %)
  2. Monto total prestado
  3. Tiempo en años del préstamo hipotecario
  4. Cuántos pagos ya has realizado (en meses)
  5. Monto a abonar (abono extra a capital)

La lógica de cálculo vive en mortgage.py y también es usada por la
aplicación web (app.py).
"""

from mortgage import calcular_resultado, PrestamoError


def pedir_numero(mensaje: str, minimo: float = 0, permitir_cero: bool = False) -> float:
    """Solicita un número al usuario validando que sea válido y positivo."""
    while True:
        entrada = input(mensaje).strip().replace(",", "")
        try:
            valor = float(entrada)
        except ValueError:
            print("  -> Por favor ingresa un número válido.")
            continue
        if valor < minimo or (valor == 0 and not permitir_cero):
            print(f"  -> El valor debe ser mayor a {minimo}.")
            continue
        return valor


def pedir_entero(mensaje: str, minimo: int = 0) -> int:
    """Solicita un número entero al usuario validando que sea válido."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print("  -> Por favor ingresa un número entero válido.")
            continue
        if valor < minimo:
            print(f"  -> El valor debe ser mayor o igual a {minimo}.")
            continue
        return valor


def formatear_dinero(valor: float) -> str:
    return f"${valor:,.2f}"


def main():
    print("=" * 60)
    print(" CALCULADORA DE AHORRO EN PRÉSTAMO HIPOTECARIO")
    print("=" * 60)
    print()

    tasa_anual = pedir_numero("Tasa actual del préstamo (anual, en %): ")
    monto_prestado = pedir_numero("Monto total prestado: ")
    anios = pedir_numero("Tiempo en años del préstamo hipotecario: ")
    pagos_realizados = pedir_entero(
        "Cuántos pagos has realizado a tu préstamo hipotecario (en meses): "
    )
    monto_abonar = pedir_numero("Monto a abonar (abono extra a capital): ")

    try:
        r = calcular_resultado(tasa_anual, monto_prestado, anios, pagos_realizados, monto_abonar)
    except PrestamoError as e:
        print(f"\n{e}")
        return

    print("\n" + "=" * 60)
    print(" RESUMEN DEL PRÉSTAMO")
    print("=" * 60)
    print(f"Cuota mensual actual:            {formatear_dinero(r.cuota)}")
    print(f"Saldo pendiente actual:          {formatear_dinero(r.saldo_actual)}")
    print(f"Meses restantes (sin abono):     {r.meses_sin_abono} meses "
          f"({r.meses_sin_abono / 12:.1f} años)")
    print(f"Intereses restantes (sin abono): {formatear_dinero(r.interes_sin_abono)}")

    print("\n" + "-" * 60)
    print(f" SI ABONAS {formatear_dinero(monto_abonar)} AL CAPITAL")
    print("-" * 60)
    print(f"Nuevo saldo pendiente:           {formatear_dinero(r.saldo_con_abono)}")
    print(f"Meses restantes (con abono):     {r.meses_con_abono} meses "
          f"({r.meses_con_abono / 12:.1f} años)")
    print(f"Intereses restantes (con abono): {formatear_dinero(r.interes_con_abono)}")

    print("\n" + "=" * 60)
    print(" AHORROS OBTENIDOS")
    print("=" * 60)
    print(f"Ahorro en intereses:             {formatear_dinero(r.ahorro_interes)}"
          f"  ({r.porcentaje_ahorro_interes:.2f}%)")
    print(f"Reducción del plazo:             {r.reduccion_meses} meses "
          f"({r.reduccion_meses / 12:.1f} años)  ({r.porcentaje_reduccion_tiempo:.2f}%)")
    print("=" * 60)


if __name__ == "__main__":
    main()

