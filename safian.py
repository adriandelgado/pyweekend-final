from datetime import datetime, date, time
import pygame, sys

SLICE_TIMESTAMP = slice(0, 10)
SLICE_MAC_AP = slice(11, 26)
SLICE_MAC_CLIENTE = slice(27, 42)
INICIO_JORNADA = time(8, 0)
FIN_JORNADA = time(17, 30)


def diccAPs(cuartos_espol):
    with open(cuartos_espol) as cuartos_csv:
        next(cuartos_csv)
        dic_cuartos = dict()
        for linea in cuartos_csv:
            cuarto, _, mac1, mac2, mac3 = linea.rstrip().split(",")
            dic_cuartos[str(sorted([mac1, mac2, mac3]))] = cuarto
    return dic_cuartos


def generar_animacion(dataset, cuartos_espol, personas, inicio, rango):
    """
    Para un rango específico de horas-minutos, mostrar una animación
    del movimiento (cambio de cuartos) en el edificio para una lista
    de hasta 5 personas (especificadas por el usuario).
    Como respuesta a esta tarea debe adjuntar el video de la animación,
    la misma que debe tener una duración máxima de 1 minuto.
    """
    COORDENADAS = {
        "c-001": (75, 60),
        "c-002": (200, 95),
        "c-003": (400, 90),
        "c-004": (81, 220),
        "c-005": (415, 200),
        "c-006": (625, 80),
        "c-007": (840, 100),
        "c-008": (1000, 80),
        "c-009": (650, 230),
        "c-010": (970, 230),
    }
    SLICE_TIMESTAMP = slice(0, 10)
    SLICE_MAC_AP = slice(11, 26)
    SLICE_MAC_CLIENTE = slice(27, 42)
    ROJO = (255, 0, 0)

    dicAp = diccAPs(cuartos_espol)
    diccionario = dict()

    # Obtener posiciones por segunto o timestamp
    with open(dataset) as ds:
        next(ds)
        for linea in ds:
            tiempo = int(linea[SLICE_TIMESTAMP])

            macCliente = linea[SLICE_MAC_CLIENTE]
            if (macCliente in personas) and (inicio <= tiempo <= (inicio + rango)):
                macAp = linea[SLICE_MAC_AP]
                try:
                    if macCliente not in diccionario[tiempo]:
                        diccionario[tiempo].setdefault(macCliente, {macAp})
                    elif (
                        macCliente in diccionario[tiempo]
                        and len(diccionario[tiempo][macCliente]) < 3
                    ):
                        diccionario[tiempo][macCliente].add(macAp)
                except:
                    diccionario.setdefault(tiempo, dict()).setdefault(
                        macCliente, {macAp}
                    )

    pygame.init()

    screen = pygame.display.set_mode((1084, 304))
    pygame.display.set_caption("Rastreador de cliente")
    image = pygame.image.load("Mapa.PNG")
    screen.blit(image, (0, 0))
    pygame.display.update()

    clock = pygame.time.Clock()
    a = True
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(0)

        # Intento de ubicar rectángulos en cada macAp pero crashea
        a = False
        for tiempo in range(inicio + rango):
            try:
                screen.blit(image, (0, 0))
                pygame.display.update()
                for mac in diccionario[tiempo]:
                    cuarto = diccAPs(diccionario[tiempo][mac])
                    x, y = COORDENADAS[cuarto]
                    pygame.draw.rect(screen, ROJO, (x, y, 15, 15))
                pygame.display.update()
            except:
                screen.blit(image, (0, 0))
                pygame.display.update()

        # Añadir texto:          #Fuente,Tamaño de letra
        fuenteConsistema = pygame.font.SysFont("Arial", 5)
        fuente = pygame.font.Font(None, 10)
        #                               TEXTO ,-,Color de letra, Color de Fondo del texto
        texto = fuente.render("Prueba Fuentes", 0, ROJO, CIAN)
        # Si usamos un color de fondo de texto opuesto al de la letra un mas oscuro que el blanco nos ahorramos es graficar la figura geométrica y solo ponemos el texto con el AP

        # Ubicar texto:
        screen.blit(texto, (x, y))
        pygame.display.update()


generar_animacion(
    "logs-conexion.csv",
    "cuartos_espol.csv",
    ["4888CA:6E:14:6C", "388C50:9E:A5:D8", "388C50:9E:A5:D8"],
    1607173200,
    80,
)
