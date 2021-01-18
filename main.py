from funciones import (
    flujo_personas,
    triangulacion,
    alertas_aforo,
    generar_animacion,
    alertavista,
    alertas_tiempo_real,
)
from datetime import date, datetime

# # Tarea 1
# dia = date(2020, 12, 5)
# num = flujo_personas("logs-conexion.csv", dia)
# print(num)

# # Tarea 2
# t = triangulacion(
#     "logs-conexion.csv", "cuartos_espol.csv", "94AE61:70:C6:9B", "1607209224"
# )
# print(t)

# # Tarea 3
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-010"), sep="\n")

# Tarea 4
dimensiones = {
    "c-001": {"ancho": (10, 110), "altura": (10, 110)},
    "c-002": {"ancho": (180, 300), "altura": (10, 110)},
    "c-003": {"ancho": (370, 460), "altura": (10, 110)},
    "c-004": {"ancho": (10, 220), "altura": (190, 250)},
    "c-005": {"ancho": (290, 450), "altura": (190, 250)},
    "c-006": {"ancho": (530, 630), "altura": (10, 110)},
    "c-007": {"ancho": (700, 820), "altura": (10, 110)},
    "c-008": {"ancho": (890, 980), "altura": (10, 110)},
    "c-009": {"ancho": (520, 730), "altura": (190, 250)},
    "c-010": {"ancho": (800, 980), "altura": (190, 250)},
}

lista = [
    "04FE31:54:79:C6",
    "ACF7F3:AA:D1:B4",
    "0022A6:1C:FE:3E",
    "20F3A3:C7:5E:E7",
]
dataset = "logs-conexion.csv"
cuartos_espol = "cuartos_espol.csv"
inicio = datetime(2020, 12, 5, 9, 0)
fin = datetime(2020, 12, 5, 10, 0)
# generar_animacion(dataset, cuartos_espol, lista, inicio, fin, dimensiones)

# # Tarea 5
# alertavista(
#     "logs-conexion.csv",
#     "cuartos_espol.csv",
#     datetime(2020, 12, 5, 12, 0),
#     datetime(2020, 12, 5, 12, 30),
# )


# # Tarea 6
# alertas_tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-008")

abierto = True
while abierto:
    num_tarea = int(
        input(
            """¿Qué tarea desea probar? (ingrese un dígito)
    Tarea 1: flujo_personas
    Tarea 2: triangulacion
    Tarea 3: alertas_aforo
    Tarea 4: animacion movimiento
    Tarea 5: contador minuto a minuto
    Tarea 6: contador theLegion\n
    """
        )
    )
    if num_tarea == 1:
        fecha = input("Ingrese una fecha en el formato: YYYY-MM-DD: ")
        dia = date.fromisoformat(fecha)
        num = flujo_personas("logs-conexion.csv", dia)
        print(num)
    elif num_tarea == 2:
        mac_cliente = input("Ingrese MAC del cliente: ")
        timestamp = input("Ingrese timestamp: ")
        t = triangulacion(
            "logs-conexion.csv", "cuartos_espol.csv", mac_cliente, timestamp
        )
        print(t)

    elif num_tarea == 3:
        cuarto = input("Ingrese cuarto: ")
        print(
            *alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", cuarto), sep="\n"
        )
    elif num_tarea == 4:
        print("Mostrando reporte desde las 9am hasta 10am")
        generar_animacion(dataset, cuartos_espol, lista, inicio, fin, dimensiones)
    elif num_tarea == 5:
        print("Mostrando reporte desde las 12 hasta 12:30")
        alertavista(
            "logs-conexion.csv",
            "cuartos_espol.csv",
            datetime(2020, 12, 5, 12, 0),
            datetime(2020, 12, 5, 12, 30),
        )
    elif num_tarea == 6:
        cuarto = input("Ingrese cuarto: ")
        alertas_tiempo_real("logs-conexion.csv", "cuartos_espol.csv", cuarto)
    else:
        print("El número debe estar entre 1 y 6")

    if input("¿Desea Continuar? (si/no)").lower() == "no":
        abierto = False