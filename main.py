from funciones import (
    flujo_personas,
    triangulacion,
    alertas_aforo,
    reporte_rango,
    tiempo_real,
)
from datetime import date, datetime
from timeit import default_timer as timer
import matplotlib.pyplot as plt
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
# lista_personas = [
#     "04FE31:54:79:C6",
#     "ACF7F3:AA:D1:B4",
#     "0022A6:1C:FE:3E",
#     "20F3A3:C7:5E:E7",
# ]
# generador = generar_datos(
#     "logs-conexion.csv",
#     "cuartos_espol.csv",
#     lista_personas,
#     datetime(2020, 12, 5, 9, 0),
#     datetime(2020, 12, 5, 10, 0),
# )
# print(next(generador))

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


# # Tarea 6
# start = timer()
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-001"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-002"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-003"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-004"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-005"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-006"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-007"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-008"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-009"), sep="\n")
# print(*tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-010"), sep="\n")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-001")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-002")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-003")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-004")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-005")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-006")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-007")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-008")
# tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-009")
# generador = tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-010")
# print(generador)
# for i in generador:
#     print(i)

# end = timer()
# print("tiempo alertas_aforo: ", end - start)

import pygame
import os

pygame.font.init()
pygame.mixer.init()

ANCHO, ALTURA = 500, 500
VENTANA = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption("Aforo")

BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
FUENTE = pygame.font.SysFont("sans-serif", 40)

FPS = 60


def draw_window(bloque):
    fecha_h, num, aforo, color = bloque
    if color == "verde":
        VENTANA.fill(VERDE)
    else:
        VENTANA.fill(ROJO)
    tiempo = FUENTE.render(fecha_h, 1, BLANCO)
    numero_personas = FUENTE.render(num, 1, BLANCO)
    aforo_cuarto = FUENTE.render(aforo, 1, BLANCO)
    VENTANA.blit(tiempo, ((ANCHO - tiempo.get_width()) / 2, ALTURA / 2 - 150))
    VENTANA.blit(
        numero_personas, ((ANCHO - numero_personas.get_width()) / 2, ALTURA / 2 - 100)
    )
    VENTANA.blit(
        aforo_cuarto, ((ANCHO - aforo_cuarto.get_width()) / 2, ALTURA / 2 + 100)
    )

    pygame.display.update()


def main():
    # clock = pygame.time.Clock()
    run = True
    generador = tiempo_real("logs-conexion.csv", "cuartos_espol.csv", "c-008")
    while run:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window(next(generador))

    main()


if __name__ == "__main__":
    main()