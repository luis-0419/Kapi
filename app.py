"""
Aplicación web Flask para la Calculadora de Préstamo Hipotecario.

Muestra un formulario para ingresar los datos del préstamo y calcula
el ahorro en intereses y la reducción del plazo al hacer un abono
extra a capital.
"""

from flask import Flask, render_template, request

from mortgage import calcular_resultado, PrestamoError

app = Flask(__name__)


def _to_float(valor: str) -> float:
    return float(valor.strip().replace(",", ""))


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None
    datos = {
        "tasa_anual": "",
        "monto_prestado": "",
        "anios": "",
        "pagos_realizados": "",
        "monto_abonar": "",
    }

    if request.method == "POST":
        datos = {
            "tasa_anual": request.form.get("tasa_anual", ""),
            "monto_prestado": request.form.get("monto_prestado", ""),
            "anios": request.form.get("anios", ""),
            "pagos_realizados": request.form.get("pagos_realizados", ""),
            "monto_abonar": request.form.get("monto_abonar", ""),
        }

        try:
            tasa_anual = _to_float(datos["tasa_anual"])
            monto_prestado = _to_float(datos["monto_prestado"])
            anios = _to_float(datos["anios"])
            pagos_realizados = int(float(datos["pagos_realizados"]))
            monto_abonar = _to_float(datos["monto_abonar"])

            if tasa_anual <= 0 or monto_prestado <= 0 or anios <= 0:
                raise PrestamoError("La tasa, el monto y el plazo deben ser mayores a 0.")
            if pagos_realizados < 0:
                raise PrestamoError("Los pagos realizados no pueden ser negativos.")
            if monto_abonar <= 0:
                raise PrestamoError("El monto a abonar debe ser mayor a 0.")

            resultado = calcular_resultado(
                tasa_anual, monto_prestado, anios, pagos_realizados, monto_abonar
            )
        except PrestamoError as e:
            error = str(e)
        except (ValueError, TypeError):
            error = "Por favor completa todos los campos con valores numéricos válidos."

    return render_template("index.html", resultado=resultado, error=error, datos=datos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
