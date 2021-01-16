from funciones import flujo_personas, triangulacion, alertas_aforo, reporte_rango
from datetime import date, datetime
from timeit import default_timer as timer

from animacion import generar_datos

# # Tarea 1
# start = timer()
# dia = date(2020, 12, 5)
# num = flujo_personas("logs-conexion.csv", dia)
# end = timer()
# print(num, "tiempo flujo_personas: ", end - start)

# # Tarea 2
# start = timer()
# t = triangulacion(
#     "logs-conexion.csv", "cuartos_espol.csv", "94AE61:70:C6:9B", "1607209224"
# )
# end = timer()
# print(t, "tiempo triangulación:", end - start)

# # Tarea 3
# start = timer()
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-001"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-002"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-003"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-004"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-005"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-006"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-007"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-008"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-009"), sep="\n")
# # print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-010"), sep="\n")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-001")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-002")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-003")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-004")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-005")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-006")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-007")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-008")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-009")
# alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-010")
# end = timer()
# print("tiempo alertas_aforo: ", end - start)

# # Tarea 4
lista_personas = [
    "04FE31:54:79:C6",
    "ACF7F3:AA:D1:B4",
    "0022A6:1C:FE:3E",
    "20F3A3:C7:5E:E7",
]
generador = generar_datos(
    "logs-conexion.csv",
    "cuartos_espol.csv",
    lista_personas,
    datetime(2020, 12, 5, 9, 0),
    datetime(2020, 12, 5, 10, 0),
)
print(next(generador))

# # Tarea 5
# start = timer()
# generador = reporte_rango(
#     "logs-conexion.csv",
#     "cuartos_espol.csv",
#     datetime(2020, 12, 5, 9, 0),
#     datetime(2020, 12, 5, 10, 0),
# )
# for minuto in generador:
#     print(minuto)
# end = timer()
# print("tiempo reporte_completo: ", end - start)
