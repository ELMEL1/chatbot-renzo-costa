import json
import os
import random
import re
import tempfile
import threading
import unicodedata
from difflib import SequenceMatcher


RUTA_BASE = os.path.dirname(__file__)
RUTA_METRICAS = os.path.join(RUTA_BASE, "metrics.json")
METRICAS_LOCK = threading.Lock()
WHATSAPP_ASESOR = "https://wa.me/51900000004?text=Hola%2C%20necesito%20comunicarme%20con%20un%20asesor%20de%20Renzo%20Costa."

STOPWORDS = {
    "a", "al", "algo", "como", "con", "cual", "cuales", "cuando",
    "de", "del", "donde", "el", "en", "es", "esta", "estan", "hay",
    "la", "las", "lo", "los", "me", "mi", "mis", "o", "para", "por",
    "puedo", "que", "quiero", "se", "si", "sobre", "su", "sus", "tienen",
    "un", "una", "y"
}

SINONIMOS = {
    "presio": "precio",
    "precioo": "precio",
    "orario": "horario",
    "orarios": "horarios",
    "debolucion": "devolucion",
    "deboluciones": "devoluciones",
    "devolusion": "devolucion",
    "promosion": "promocion",
    "promosiones": "promocion",
    "promos": "promocion",
    "delyvery": "delivery",
    "deliveri": "delivery",
    "envio": "delivery",
    "envios": "delivery",
    "pedido": "seguimiento",
    "orden": "seguimiento",
    "reclamo": "reclamos",
    "queja": "reclamos",
    "taya": "talla",
    "tallas": "talla",
    "material": "materiales"
}

PRODUCTOS = {
    "billeteras": {
        "aliases": ["billetera", "billeteras"],
        "tipos": "Tenemos billeteras clasicas, compactas, tarjeteros y modelos para dama y caballero.",
        "precio": "Las billeteras suelen estar entre S/ 89 y S/ 189, segun el modelo, tamano y tipo de cuero.",
        "materiales": "Las billeteras se ofrecen principalmente en cuero y materiales seleccionados, segun la coleccion."
    },
    "carteras": {
        "aliases": ["cartera", "carteras"],
        "tipos": "Tenemos carteras pequenas, medianas, grandes, de mano y con correa para distintas ocasiones.",
        "precio": "Las carteras suelen estar entre S/ 129 y S/ 399, dependiendo del tamano, diseno, material y temporada.",
        "materiales": "Las carteras pueden estar elaboradas en cuero y materiales seleccionados, segun el modelo."
    },
    "bolsos": {
        "aliases": ["bolso", "bolsos", "bolsa", "bolsas"],
        "tipos": "Tenemos bolsos pequenos, medianos, grandes, de hombro y modelos para uso diario.",
        "precio": "Los bolsos suelen estar entre S/ 149 y S/ 449, segun el tamano, acabado y coleccion.",
        "materiales": "Los bolsos pueden estar elaborados en cuero y otros materiales seleccionados segun la coleccion."
    },
    "correas": {
        "aliases": ["correa", "correas", "cinturon", "cinturones"],
        "tipos": "Tenemos correas casuales y formales, con distintos tipos de hebilla y acabados.",
        "precio": "Las correas suelen estar entre S/ 59 y S/ 159, dependiendo del tipo de cuero, hebilla y diseno.",
        "materiales": "Las correas se ofrecen principalmente en cuero, con diferentes acabados y hebillas."
    },
    "zapatos": {
        "aliases": ["zapato", "zapatos", "calzado"],
        "tipos": "Tenemos calzado casual, formal y modelos de temporada para dama y caballero.",
        "precio": "El calzado suele estar entre S/ 179 y S/ 499, dependiendo del modelo, material y temporada.",
        "materiales": "El calzado puede combinar cuero, forros y suelas seleccionadas segun el modelo."
    },
    "mochilas": {
        "aliases": ["mochila", "mochilas"],
        "tipos": "Tenemos mochilas urbanas, ejecutivas y modelos con varios compartimentos.",
        "precio": "Las mochilas suelen estar entre S/ 199 y S/ 499, segun el material, tamano y compartimentos.",
        "materiales": "Las mochilas pueden estar elaboradas en cuero y materiales resistentes segun el modelo."
    },
    "maletines": {
        "aliases": ["maletin", "maletines", "portafolio", "portafolios"],
        "tipos": "Tenemos maletines ejecutivos, portafolios y modelos para laptop.",
        "precio": "Los maletines suelen estar entre S/ 249 y S/ 599, dependiendo del tamano, cuero y diseno.",
        "materiales": "Los maletines pueden estar elaborados en cuero y materiales seleccionados para uso ejecutivo."
    }
}


def cargar_intenciones():
    with open(os.path.join(RUTA_BASE, "intents.json"), "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")
    texto = re.sub(r"[^a-z0-9ñ\s]", " ", texto)
    return " ".join(texto.split())


def obtener_palabras(texto):
    palabras = []

    for palabra in normalizar_texto(texto).split():
        palabra = SINONIMOS.get(palabra, palabra)
        if palabra not in STOPWORDS and len(palabra) > 1:
            palabras.append(palabra)

    return palabras


def detectar_producto(mensaje):
    palabras = set(obtener_palabras(mensaje))

    for nombre, producto in PRODUCTOS.items():
        if palabras.intersection(producto["aliases"]):
            return nombre

    return None


def detectar_detalle_producto(mensaje):
    palabras = set(obtener_palabras(mensaje))

    if palabras.intersection({"precio", "precios", "costo", "costos", "valor"}):
        return "precio"
    if palabras.intersection({"materiales", "cuero", "calidad", "fabricado", "hecho"}):
        return "materiales"
    if palabras.intersection({"tipo", "tipos", "modelo", "modelos", "opciones", "variedad"}):
        return "tipos"
    if palabras.intersection({"promocion", "oferta", "ofertas", "descuento", "descuentos"}):
        return "promociones"

    return None


def respuesta_detalle_producto(producto, detalle):
    nombre = producto.capitalize()

    if detalle == "promociones":
        return (
            f"Las promociones de {producto} cambian segun la temporada y disponibilidad. "
            "Te recomiendo consultar las ofertas vigentes en la tienda o canal oficial."
        )

    respuesta = PRODUCTOS[producto][detalle]
    nota = ""
    if detalle == "precio":
        nota = (
            "\n\nEstos precios son referenciales para el proyecto y pueden variar "
            "por tienda, stock, promociones y temporada."
        )

    return f"{respuesta}{nota}\n\n¿Deseas conocer otra informacion sobre {nombre.lower()}?"


def respuesta_producto_seleccionado(producto):
    return (
        f"{PRODUCTOS[producto]['tipos']}\n\n"
        f"¿Que deseas conocer sobre {producto}: precios, materiales, modelos o promociones?"
    )


def similitud_palabra(palabra_usuario, palabra_patron):
    if palabra_usuario == palabra_patron:
        return 1
    if palabra_usuario in palabra_patron or palabra_patron in palabra_usuario:
        return 0.82
    return SequenceMatcher(None, palabra_usuario, palabra_patron).ratio()


def calcular_puntaje(mensaje_usuario, patron):
    mensaje_normalizado = normalizar_texto(mensaje_usuario)
    patron_normalizado = normalizar_texto(patron)

    if not patron_normalizado:
        return 0
    if mensaje_normalizado == patron_normalizado:
        return 100

    puntaje = SequenceMatcher(None, mensaje_normalizado, patron_normalizado).ratio() * 35
    if patron_normalizado in mensaje_normalizado:
        puntaje += 42

    palabras_usuario = obtener_palabras(mensaje_usuario)
    palabras_patron = obtener_palabras(patron)

    if not palabras_usuario or not palabras_patron:
        return puntaje

    coincidencias = 0
    for palabra_patron in palabras_patron:
        mejor_similitud = max(
            similitud_palabra(palabra_usuario, palabra_patron)
            for palabra_usuario in palabras_usuario
        )
        if mejor_similitud >= 0.78:
            coincidencias += mejor_similitud

    return puntaje + (coincidencias / len(palabras_patron)) * 55


def detectar_intencion(mensaje, intenciones):
    mejor_intencion = None
    mejor_puntaje = 0

    for intencion in intenciones["intents"]:
        if intencion["tag"] == "desconocido":
            continue

        puntaje = max(
            (calcular_puntaje(mensaje, patron) for patron in intencion["patterns"]),
            default=0
        )
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_intencion = intencion

    if mejor_intencion and mejor_puntaje >= 38:
        return mejor_intencion

    return next(
        (intencion for intencion in intenciones["intents"] if intencion["tag"] == "desconocido"),
        None
    )


def actualizar_metricas(tag):
    with METRICAS_LOCK:
        try:
            with open(RUTA_METRICAS, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {"total_consultas": 0}

        datos["total_consultas"] = datos.get("total_consultas", 0) + 1
        datos[tag] = datos.get(tag, 0) + 1

        descriptor, ruta_temporal = tempfile.mkstemp(
            prefix="metrics_",
            suffix=".json",
            dir=RUTA_BASE,
            text=True
        )

        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
                archivo.flush()
                os.fsync(archivo.fileno())

            os.replace(ruta_temporal, RUTA_METRICAS)
        finally:
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)


def construir_resultado(respuesta, intencion, contexto, accion=None):
    actualizar_metricas(intencion)
    resultado = {
        "respuesta": respuesta,
        "intencion": intencion,
        "contexto": contexto
    }

    if accion:
        resultado["accion"] = accion

    return resultado


def intencion_para_detalle(detalle):
    return {
        "precio": "precios",
        "materiales": "materiales",
        "promociones": "promociones",
        "tipos": "productos"
    }[detalle]


def obtener_respuesta(mensaje_usuario, contexto=None):
    contexto = dict(contexto or {})
    mensaje_limpio = normalizar_texto(mensaje_usuario)

    if not mensaje_limpio:
        return {
            "respuesta": "Por favor, escribe una consulta para poder ayudarte.",
            "intencion": "vacio",
            "contexto": contexto
        }

    intenciones = cargar_intenciones()
    producto = detectar_producto(mensaje_limpio)
    detalle = detectar_detalle_producto(mensaje_limpio)
    producto_contexto = contexto.get("producto")
    tema_contexto = contexto.get("tema")

    if producto:
        contexto["producto"] = producto

        if detalle:
            contexto.update({"tema": detalle, "opcion_esperada": "detalle_producto"})
            return construir_resultado(
                respuesta_detalle_producto(producto, detalle),
                intencion_para_detalle(detalle),
                contexto
            )

        if tema_contexto == "precios":
            contexto.update({"tema": "precios", "opcion_esperada": "detalle_producto"})
            return construir_resultado(
                respuesta_detalle_producto(producto, "precio"),
                "precios",
                contexto
            )

        contexto.update({"tema": "productos", "opcion_esperada": "detalle_producto"})
        return construir_resultado(
            respuesta_producto_seleccionado(producto),
            "productos",
            contexto
        )

    if producto_contexto and detalle:
        contexto.update({"tema": detalle, "opcion_esperada": "detalle_producto"})
        return construir_resultado(
            respuesta_detalle_producto(producto_contexto, detalle),
            intencion_para_detalle(detalle),
            contexto
        )

    intencion = detectar_intencion(mensaje_limpio, intenciones)
    tag = intencion["tag"]

    if tag == "productos":
        contexto = {"tema": "productos", "opcion_esperada": "producto"}
        respuesta = (
            "Tenemos carteras, billeteras, bolsos, correas, zapatos, mochilas y "
            "maletines. ¿Que producto te interesa?"
        )
    elif tag == "precios":
        contexto = {"tema": "precios", "opcion_esperada": "producto"}
        respuesta = (
            "Puedo darte precios referenciales de carteras, billeteras, bolsos, "
            "correas, zapatos, mochilas y maletines. ¿Que producto deseas consultar?"
        )
    else:
        contexto["tema"] = tag
        contexto.pop("opcion_esperada", None)
        respuesta = random.choice(intencion["responses"])

    accion = None
    if tag == "contacto":
        respuesta = (
            "Para una atencion mas rapida, comunicate con uno de nuestros asesores "
            "por WhatsApp. Si tu consulta es por un pedido, reclamo o garantia, "
            "ten a la mano tu comprobante o numero de orden."
        )
        accion = {
            "tipo": "whatsapp",
            "etiqueta": "Escribir a un asesor",
            "url": WHATSAPP_ASESOR
        }

    return construir_resultado(respuesta, tag, contexto, accion=accion)
