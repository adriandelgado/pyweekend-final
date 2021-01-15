from funciones import flujo_personas, triangulacion, alertas_aforo, reporte_completo
from datetime import date
from timeit import default_timer as timer

# Tarea 1
start = timer()
dia = date(2020, 12, 5)
num = flujo_personas("logs-conexion.csv", dia)
end = timer()
print(num, "tiempo flujo_personas: ", end - start)

# Tarea 2
start = timer()
t = triangulacion(
    "logs-conexion.csv", "cuartos_espol.csv", "94AE61:70:C6:9B", "1607209224"
)
end = timer()
print(t, "tiempo triangulación:", end - start)

# Tarea 3
start = timer()
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-001"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-002"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-003"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-004"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-005"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-006"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-007"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-008"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-009"), sep="\n")
# print(*alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-010"), sep="\n")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-001")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-002")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-003")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-004")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-005")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-006")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-007")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-008")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-009")
alertas_aforo("logs-conexion.csv", "cuartos_espol.csv", "c-010")
end = timer()
print("tiempo alertas_aforo: ", end - start)

# Tarea 5
start = timer()
reporte_completo("logs-conexion.csv", "cuartos_espol.csv")
end = timer()
print("tiempo reporte_completo: ", end - start)
