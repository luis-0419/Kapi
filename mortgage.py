"""
Lógica de cálculo para préstamos hipotecarios.

Este módulo contiene funciones puras (sin entrada/salida) para calcular
la cuota mensual, el saldo pendiente y simular la amortización de un
préstamo hipotecario, incluyendo el efecto de abonos extra a capital.
Es utilizado tanto por la versión de consola (calculadora_hipoteca.py)
como por la aplicación web (app.py).
"""

from dataclasses import dataclass


class PrestamoError(Exception):
    """Error de validación o cálculo relacionado con el préstamo."""


def calcular_cuota(principal: float, tasa_mensual: float, n_pagos: int) -> float:
    """Calcula la cuota mensual fija de un préstamo con amortización francesa."""
    if n_pagos <= 0:
        raise PrestamoError("El número de pagos debe ser mayor a 0.")
    if tasa_mensual == 0:
        return principal / n_pagos
    factor = (1 + tasa_mensual) ** n_pagos
    return principal * tasa_mensual * factor / (factor - 1)


def saldo_despues_de_pagos(principal: float, tasa_mensual: float, cuota: float, pagos: int) -> float:
    """Calcula el saldo restante del préstamo luego de 'pagos' cuotas pagadas."""
    saldo = principal
    for _ in range(pagos):
        interes_mes = saldo * tasa_mensual
        abono_capital = cuota - interes_mes
        saldo -= abono_capital
        if saldo < 0:
            saldo = 0
    return saldo


def simular_amortizacion(saldo_inicial: float, tasa_mensual: float, cuota: float):
    """
    Simula el pago de un préstamo con cuota fija hasta saldarlo por completo.
    Devuelve (meses_para_pagar, interes_total_pagado).
    """
    saldo = saldo_inicial
    meses = 0
    interes_total = 0.0

    if saldo <= 0:
        return 0, 0.0

    while saldo > 0.01:
        interes_mes = saldo * tasa_mensual
        abono_capital = cuota - interes_mes

        if abono_capital <= 0:
            raise PrestamoError(
                "La cuota actual no alcanza a cubrir los intereses; "
                "el préstamo nunca se terminaría de pagar."
            )

        if abono_capital >= saldo:
            interes_total += interes_mes
            saldo = 0
        else:
            saldo -= abono_capital
            interes_total += interes_mes

        meses += 1

    return meses, interes_total


@dataclass
class ResultadoHipoteca:
    cuota: float
    saldo_actual: float
    meses_sin_abono: int
    interes_sin_abono: float
    saldo_con_abono: float
    meses_con_abono: int
    interes_con_abono: float
    ahorro_interes: float
    reduccion_meses: int
    porcentaje_ahorro_interes: float
    porcentaje_reduccion_tiempo: float


def calcular_resultado(
    tasa_anual: float,
    monto_prestado: float,
    anios: float,
    pagos_realizados: int,
    monto_abonar: float,
) -> ResultadoHipoteca:
    """Ejecuta todo el cálculo de ahorro por abono a capital y devuelve el resultado."""
    tasa_mensual = (tasa_anual / 100) / 12
    n_meses_total = int(round(anios * 12))

    if pagos_realizados >= n_meses_total:
        raise PrestamoError(
            "El número de pagos realizados debe ser menor al plazo total del préstamo."
        )

    cuota = calcular_cuota(monto_prestado, tasa_mensual, n_meses_total)
    saldo_actual = saldo_despues_de_pagos(monto_prestado, tasa_mensual, cuota, pagos_realizados)

    if monto_abonar > saldo_actual:
        raise PrestamoError(
            f"El monto a abonar (${monto_abonar:,.2f}) es mayor al saldo actual del "
            f"préstamo (${saldo_actual:,.2f})."
        )

    meses_sin_abono, interes_sin_abono = simular_amortizacion(saldo_actual, tasa_mensual, cuota)

    saldo_con_abono = saldo_actual - monto_abonar
    meses_con_abono, interes_con_abono = simular_amortizacion(saldo_con_abono, tasa_mensual, cuota)

    ahorro_interes = interes_sin_abono - interes_con_abono
    reduccion_meses = meses_sin_abono - meses_con_abono

    porcentaje_ahorro_interes = (
        (ahorro_interes / interes_sin_abono * 100) if interes_sin_abono > 0 else 0.0
    )
    porcentaje_reduccion_tiempo = (
        (reduccion_meses / meses_sin_abono * 100) if meses_sin_abono > 0 else 0.0
    )

    return ResultadoHipoteca(
        cuota=cuota,
        saldo_actual=saldo_actual,
        meses_sin_abono=meses_sin_abono,
        interes_sin_abono=interes_sin_abono,
        saldo_con_abono=saldo_con_abono,
        meses_con_abono=meses_con_abono,
        interes_con_abono=interes_con_abono,
        ahorro_interes=ahorro_interes,
        reduccion_meses=reduccion_meses,
        porcentaje_ahorro_interes=porcentaje_ahorro_interes,
        porcentaje_reduccion_tiempo=porcentaje_reduccion_tiempo,
    )
