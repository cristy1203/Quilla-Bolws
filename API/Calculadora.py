from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape


# 1. DICCIONARIOS DE PRECIOS BASE
MENU_PLATOS = {
    "1": {
        "nombre": "Desayuno Caribeño Típico",
        "precio": 12000
    },
    "2": {
        "nombre": "Almuerzo Casero",
        "precio": 16000
    },
    "3": {
        "nombre": "Especial / Asado al Carbón",
        "precio": 20000
    }
}

ADICIONES_TIPICAS = {
    "queso": {
        "nombre": "Queso costeño extra",
        "precio": 3000
    },
    "suero": {
        "nombre": "Suero atollabuey",
        "precio": 2000
    },
    "jugo": {
        "nombre": "Jugo natural / Guarapo",
        "precio": 4000
    },
    "chicharron": {
        "nombre": "Chicharrón crocante",
        "precio": 5000
    }
}

COSTO_DOMICILIO_BARRANQUILLA = 5000


# 2. FORMATEAR MONEDA COLOMBIANA
def formatear_cop(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


# 3. FUNCIÓN PRINCIPAL DE CÁLCULO
def calcular_cotizacion(
    opcion_plato,
    cantidad,
    adiciones_elegidas,
    es_domicilio
):
    # Si el plato no existe, se utiliza el almuerzo por defecto
    plato = MENU_PLATOS.get(opcion_plato, MENU_PLATOS["2"])

    precio_unitario = plato["precio"]
    nombre_plato = plato["nombre"]

    # Mantener el límite original de 1 a 50 porciones
    if cantidad < 1:
        cantidad = 1
    elif cantidad > 50:
        cantidad = 50

    # Calcular las adiciones por plato
    costo_extras_por_plato = 0
    nombres_adiciones = []

    for clave in adiciones_elegidas:
        if clave in ADICIONES_TIPICAS:
            costo_extras_por_plato += ADICIONES_TIPICAS[clave]["precio"]
            nombres_adiciones.append(
                ADICIONES_TIPICAS[clave]["nombre"]
            )

    # Calcular domicilio
    costo_envio = (
        COSTO_DOMICILIO_BARRANQUILLA
        if es_domicilio
        else 0
    )

    # Operaciones originales
    subtotal_platos = precio_unitario * cantidad
    total_adiciones = costo_extras_por_plato * cantidad
    total_final = subtotal_platos + total_adiciones + costo_envio

    return {
        "orden": f"{cantidad}x {nombre_plato}",
        "adiciones": (
            ", ".join(nombres_adiciones)
            if nombres_adiciones
            else "Ninguna"
        ),
        "entrega": (
            "Domicilio Barranquilla"
            if es_domicilio
            else "Recoger en Punto"
        ),
        "subtotal_platos": subtotal_platos,
        "total_adiciones": total_adiciones,
        "costo_envio": costo_envio,
        "total_final": total_final
    }


# 4. PÁGINA DE RESULTADOS
def pagina_resultado(resultado):

    contenido = f"""
    <div class="resultado">
        <span class="etiqueta">QUILLA BOWLS</span>

        <h1>Resumen de tu cotización</h1>

        <p class="descripcion">
            Este es el detalle del pedido que has calculado.
        </p>

        <div class="detalle">
            <div class="fila">
                <span>Orden seleccionada</span>
                <strong>{escape(resultado["orden"])}</strong>
            </div>

            <div class="fila">
                <span>Adiciones típicas</span>
                <strong>{escape(resultado["adiciones"])}</strong>
            </div>

            <div class="fila">
                <span>Método de entrega</span>
                <strong>{escape(resultado["entrega"])}</strong>
            </div>

            <div class="fila">
                <span>Subtotal de platos</span>
                <strong>{formatear_cop(resultado["subtotal_platos"])}</strong>
            </div>

            <div class="fila">
                <span>Total de adiciones</span>
                <strong>{formatear_cop(resultado["total_adiciones"])}</strong>
            </div>

            <div class="fila">
                <span>Costo de envío</span>
                <strong>{formatear_cop(resultado["costo_envio"])}</strong>
            </div>

            <div class="total">
                <span>TOTAL A PAGAR</span>
                <strong>{formatear_cop(resultado["total_final"])}</strong>
            </div>
        </div>

        <p class="nota">
            Los valores corresponden a los precios base seleccionados
            y a las adiciones y entrega indicadas.
        </p>

        <a class="boton" href="/#calculadora">
            Volver a la calculadora
        </a>
    </div>
    """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cotización | Quilla Bowls</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 30px 15px;
                font-family: Arial, sans-serif;
                background: #FDF8EE;
                color: #08252E;
            }}

            .resultado {{
                max-width: 650px;
                margin: 30px auto;
                padding: 30px;
                background: white;
                border-radius: 22px;
                border: 1px solid #F7EEDB;
                box-shadow: 0 8px 25px rgba(8, 37, 46, 0.10);
            }}

            .etiqueta {{
                display: inline-block;
                padding: 7px 13px;
                border-radius: 20px;
                background: #FCE08B;
                color: #0E3A47;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }}

            h1 {{
                color: #0E3A47;
                margin-bottom: 8px;
            }}

            .descripcion {{
                color: #52656A;
                line-height: 1.5;
            }}

            .detalle {{
                margin-top: 25px;
                border-top: 1px solid #F7EEDB;
            }}

            .fila {{
                display: flex;
                justify-content: space-between;
                gap: 15px;
                padding: 15px 0;
                border-bottom: 1px solid #F7EEDB;
                line-height: 1.4;
            }}

            .fila strong {{
                text-align: right;
                color: #114452;
            }}

            .total {{
                display: flex;
                justify-content: space-between;
                gap: 15px;
                margin-top: 18px;
                padding: 20px;
                background: #0E3A47;
                color: #FCE08B;
                border-radius: 14px;
                font-weight: bold;
                font-size: 18px;
            }}

            .total strong {{
                text-align: right;
            }}

            .nota {{
                color: #52656A;
                font-size: 13px;
                line-height: 1.5;
                margin-top: 20px; }}

            .boton {{
                display: block;
                margin-top: 25px;
                padding: 15px;
                background: #F3722C;
                color: white;
                text-align: center;
                text-decoration: none;
                font-weight: bold;
                border-radius: 12px;
            }}

            .boton:hover {{
                background: #D95B18;
            }}

            @media (max-width: 480px) {{
                .resultado {{
                    padding: 22px 17px;
                }}

                .fila {{
                    flex-direction: column;
                    gap: 5px;
                }}

                .fila strong {{
                    text-align: left;
                }}

                .total {{
                    flex-direction: column;
                    font-size: 16px;
                }}

                .total strong {{
                    text-align: left;
                }}
            }}
        </style>
    </head>

    <body>
        {contenido}
    </body>
    </html>
    """


# 5. PÁGINA DE ERROR
def pagina_error(mensaje):

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error | Quilla Bowls</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #FDF8EE;
                color: #0E3A47;
                padding: 30px 15px;
            }}

            main {{
                max-width: 550px;
                margin: 50px auto;
                padding: 30px;
                background: white;
                border-radius: 18px;
                text-align: center;
            }}

            a {{
                display: inline-block;
                margin-top: 20px;
                padding: 13px 20px;
                background: #F3722C;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
            }}
        </style>
    </head>

    <body>
        <main>
            <h1>No se pudo procesar la cotización</h1>
            <p>{escape(mensaje)}</p>
            <a href="/#calculadora">Volver a intentarlo</a>
        </main>
    </body>
    </html>
    """


# 6. FUNCIÓN PRINCIPAL PARA VERCEL
class handler(BaseHTTPRequestHandler):

    def responder(self, contenido, estado=200):

        respuesta = contenido.encode("utf-8")

        self.send_response(estado)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(respuesta))
        )
        self.end_headers()

        self.wfile.write(respuesta)

    def do_POST(self):

        try:
            longitud = int(
                self.headers.get("Content-Length", 0)
            )

            cuerpo = self.rfile.read(longitud).decode("utf-8")

            formulario = parse_qs(
                cuerpo,
                keep_blank_values=True
            )

            opcion_plato = formulario.get("plato", ["2"])[0]

            cantidad_texto = formulario.get(
                "cantidad", ["1"]
            )[0]

            adiciones_elegidas = formulario.get(
                "adiciones", []
            )

            entrega = formulario.get(
                "entrega", ["recoger"]
            )[0]

            # Validar cantidad
            try:
                cantidad = int(cantidad_texto)
            except (ValueError, TypeError):
                self.responder(
                    pagina_error("Ingresa una cantidad válida de platos."),
                    400
                )
                return

            if cantidad < 1 or cantidad > 50:
                self.responder(
                    pagina_error(
                        "La cantidad debe estar entre 1 y 50 platos."
                    ),
                    400
                )
                return

            # Validar selección de entrega
            if entrega not in ["recoger", "domicilio"]:
                self.responder(
                    pagina_error("Selecciona un método de entrega válido."),
                    400
                )
                return

            # Mantener el comportamiento original:
            # si el plato no existe, se utiliza el almuerzo.
            es_domicilio = entrega == "domicilio"

            resultado = calcular_cotizacion(
                opcion_plato,
                cantidad,
                adiciones_elegidas,
                es_domicilio
            )

            self.responder(pagina_resultado(resultado))

        except Exception:
            self.responder(
                pagina_error(
                    "Ocurrió un inconveniente. Verifica los datos e inténtalo nuevamente."
                ),
                500
            )

    def do_GET(self):

        self.send_response(303)
        self.send_header("Location", "/#calculadora")
        self.end_headers()