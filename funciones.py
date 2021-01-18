from time import sleep
from datetime import datetime, date, timedelta
from collections import defaultdict, Counter
from typing import Optional, Set, List, Dict
from random import randint
import pygame
import os
import typing as ty


SLICE_TIMESTAMP = slice(0, 10)
SLICE_MAC_AP = slice(11, 26)
SLICE_MAC_CLIENTE = slice(27, 42)

# Tarea 1
def flujo_personas(dataset: str, fecha: date) -> int:
    """
    Recibe la ubicación del dataset y una fecha y retorna la cantidad
    de personas que entraron y salieron del edificio en el día indicado
    dentro de horas laborales (8:00 - 17:30).

        Parámetros:
            dataset (str): Ubicación del log de conexiones
             fecha (date): Fecha del día a analizar

        Retorna:
            len(personas) (int): Cantidad de personas que entraron
                                 en el día indicado a partir de las 8:00
                                 pero antes de las 17:30
    """
    anio, mes, dia = fecha.year, fecha.month, fecha.day  # `año` también es aceptado
    inicio_jornada = int(datetime(anio, mes, dia, 8, 0).timestamp())
    fin_jornada = int(datetime(anio, mes, dia, 17, 30).timestamp())

    with open(dataset) as dt:
        next(dt)
        personas = set()
        for linea in dt:
            mac_cliente = linea[SLICE_MAC_CLIENTE]
            timestamp = int(linea[SLICE_TIMESTAMP])
            if inicio_jornada <= timestamp <= fin_jornada:
                personas.add(mac_cliente)
            else:
                personas.discard(mac_cliente)
    return len(personas)


# Tarea 2
# https://github.com/PyCQA/pylint/issues/3882
def triangulacion(
    dataset: str, cuartos_espol: str, mac_cliente: str, timestamp: str
) -> Optional[str]:  # pylint: disable=unsubscriptable-object
    """
    Determina el código del cuarto en el que se encuentra una MAC cliente
    en un momento (timestamp) dado.

        Parámetros:
                  dataset (str): Ubicación del log de conexiones
            cuartos_espol (str): Ubicación del archivo csv con el aforo y APs
                                 de cada cuarto
              mac_cliente (str): Dirección MAC del cliente que se desea ubicar
                timestamp (str): Segundo en que se desea realizar la ubicación
                                 (en tiempo UNIX)

        Retorna:
            cuarto (str) | None: Nombre del cuarto de la MAC si se la logra ubicar.
                                 En caso de no aparecer la MAC en el tiempo
                                 indicado se retorna None.
    """
    with open(cuartos_espol) as cuartos_csv:
        next(cuartos_csv)
        dic_cuartos = dict()
        for linea in cuartos_csv:
            cuarto, _, mac1, mac2, mac3 = linea.rstrip().split(",")
            dic_cuartos[str(sorted([mac1, mac2, mac3]))] = cuarto

    with open(dataset) as dt:
        next(dt)
        macs_ap: Set[str] = set()
        # Con el operador morsa `:=` podemos detenernos al conseguir 3 macs
        while len(macs_ap) < 3 and (linea := next(dt, "end")) != "end":
            if (
                timestamp == linea[SLICE_TIMESTAMP]
                and mac_cliente == linea[SLICE_MAC_CLIENTE]
            ):
                macs_ap.add(linea[SLICE_MAC_AP])

    if len(macs_ap) == 3:
        cuarto = dic_cuartos[str(sorted(macs_ap))]
        return cuarto
    else:
        return None


# Tarea 3
def alertas_aforo(dataset: str, cuartos_espol: str, cuarto: str) -> List[str]:
    """
    Dado un cuarto, reporta todos los momentos en los que el cuarto superó
    su aforo máximo, con un mínimo de 10 minutos entre cada alerta.

        Parámetros:
                  dataset (str): Ubicación del log de conexiones
            cuartos_espol (str): Ubicación del archivo csv con el aforo y APs
                                 de cada cuarto
                   cuarto (str): Nombre del cuarto que se desea recibir alertas

        Retorna:
            lista_alertas (list[str]): Lista de los momentos en los que el
                                       cuarto indicado superó su aforo máximo.
            Formato:
                [
                    "AAAA-MM-DD HH:MM, {cantidad} personas",
                    "AAAA-MM-DD HH:MM, {cantidad} personas",
                    ...
                ]
    """
    with open(cuartos_espol) as cuartos_csv:
        next(cuartos_csv)
        for linea in cuartos_csv:
            nombre_cuarto, aforo, mac1, mac2, mac3 = linea.rstrip().split(",")
            if nombre_cuarto == cuarto:
                aforo_max = int(aforo)
                macs_ap = {mac1, mac2, mac3}

    with open(dataset) as dt:
        next(dt)
        mismo_segundo = defaultdict(set)
        lista_alertas = []
        mac_min: Set[str] = set()
        alert_prev = datetime(1, 1, 1)

        # inicializar variables usando la primera linea
        prim_linea = next(dt)
        segundo_previo = prim_linea[SLICE_TIMESTAMP]
        minuto_previo = datetime.fromtimestamp(int(segundo_previo)).minute
        mismo_segundo[prim_linea[SLICE_MAC_CLIENTE]].add(prim_linea[SLICE_MAC_AP])

        for linea in dt:
            if segundo_previo == linea[SLICE_TIMESTAMP]:
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])
            else:
                # Añadimos el número de dispositivos que hubo en el último segundo
                for cliente, macs in mismo_segundo.items():
                    if macs == macs_ap:
                        mac_min.add(cliente)
                    else:
                        mac_min.discard(cliente)

                # Liberamos memoria y nos preparamos para la siguiente iteración
                mismo_segundo.clear()
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])

                # Checkeamos aforo cada segundo
                fecha_hr = datetime.fromtimestamp(int(segundo_previo))
                if len(mac_min) > aforo_max and fecha_hr - alert_prev >= timedelta(
                    minutes=10
                ):
                    lista_alertas.append(
                        fecha_hr.strftime("%Y-%m-%d %H:%M")
                        + f", {len(mac_min)} personas"
                    )
                    alert_prev = fecha_hr

                # Cada que pasa un minuto reiniciamos estadísticas
                timestamp = int(linea[SLICE_TIMESTAMP])
                minuto_actual = datetime.fromtimestamp(timestamp).minute
                if minuto_actual != minuto_previo:
                    minuto_previo = minuto_actual
                    mac_min.clear()

            # Al final de cada iteración actualizamos el segundo previo
            segundo_previo = linea[SLICE_TIMESTAMP]

    return lista_alertas


# Tarea 4
def generar_datos(
    dataset: str,
    cuartos_espol: str,
    personas: List[str],
    inicio: datetime,
    fin: datetime,
):
    """
    Función Interna

    Para un rango específico de horas-minutos, mostrar una animación
    del movimiento (cambio de cuartos) en el edificio para una lista
    de hasta 5 personas (especificadas por el usuario).
    Como respuesta a esta tarea debe adjuntar el video de la animación,
    la misma que debe tener una duración máxima de 1 minuto.
    """
    with open(cuartos_espol) as cuartos_csv:
        next(cuartos_csv)
        dic_cuartos = dict()
        for linea in cuartos_csv:
            nombr_cuarto, _, mac1, mac2, mac3 = linea.rstrip().split(",")
            dic_cuartos[str(sorted([mac1, mac2, mac3]))] = nombr_cuarto

    with open(dataset) as dt:
        next(dt)

        mismo_segundo = defaultdict(set)
        counter_minuto: Dict = {k: set() for k in dic_cuartos.keys()}

        # Ignorar las lineas previas al inicio solicitado
        try:
            ignorar = True
            while ignorar:
                prim_linea = next(dt)
                segundo_previo = prim_linea[SLICE_TIMESTAMP]
                if int(segundo_previo) >= inicio.timestamp():
                    ignorar = False
            minuto_previo = datetime.fromtimestamp(int(segundo_previo)).minute
            mismo_segundo[prim_linea[SLICE_MAC_CLIENTE]].add(prim_linea[SLICE_MAC_AP])
        except:
            print("Fecha de inicio fuera de registro")
            return None

        dentro_de_rango = True
        while (linea := next(dt, "end")) != "end" and dentro_de_rango:
            if segundo_previo == linea[SLICE_TIMESTAMP]:
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])
            else:
                # Añadimos el número de veces que aparece cada cuarto
                # en el diccionario `mismo_segundo`
                for cliente, macs in mismo_segundo.items():
                    for conjunto_clientes in counter_minuto.values():
                        conjunto_clientes.discard(cliente)
                    counter_minuto[str(sorted(macs))].add(cliente)

                # Liberamos memoria y nos preparamos para la siguiente iteración
                mismo_segundo.clear()
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])

                # Cada que cambia el segundo verificamos si ha pasado un minuto
                timestamp = int(linea[SLICE_TIMESTAMP])
                minuto_actual = datetime.fromtimestamp(timestamp).minute
                if timestamp > fin.timestamp():
                    dentro_de_rango = False
                elif minuto_actual != minuto_previo:
                    minuto_previo = minuto_actual
                    bloque = []
                    bloque.append(
                        datetime.fromtimestamp(int(segundo_previo)).strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    )
                    reporte = {f"c-0{i:02}": set() for i in range(1, 11)}
                    for macs_str, clientes in counter_minuto.items():
                        cuarto = dic_cuartos[macs_str]
                        for cli in clientes:
                            if cli in personas:
                                reporte[cuarto].add(cli)
                    for i in reporte.items():
                        bloque.append(i)
                    yield bloque
                    # reiniciamos el contador de gente y el reporte del minuto
                    for clientes in counter_minuto.values():
                        clientes.clear()
                    reporte.clear()
                    bloque.clear()

            # Al final de cada iteración actualizamos el segundo previo
            segundo_previo = linea[SLICE_TIMESTAMP]

    return None


def generar_animacion(
    dataset: str,
    cuartos_espol: str,
    lista: List[str],
    inicio: datetime,
    fin: datetime,
    dimensiones: dict,
):
    """
    Para un rango específico de horas-minutos, mostrar una animación
    del movimiento (cambio de cuartos) en el edificio para una lista
    de hasta 5 personas (especificadas por el usuario).
    Como respuesta a esta tarea debe adjuntar el video de la animación,
    la misma que debe tener una duración máxima de 1 minuto.
    """
    lista = lista
    generador = generar_datos(dataset, cuartos_espol, lista, inicio, fin)

    # lista para poder identificar que numero de mac ingresada se ve en la animacion
    n_mac = ["mac1", "mac2", "mac3", "mac4", "mac5"]

    pygame.init()
    FPS = 2
    clock = pygame.time.Clock()
    ANCHO, ALTURA = 1008, 282
    pantalla = pygame.display.set_mode((ANCHO, ALTURA))
    pygame.display.set_caption("Rastreo de personas")
    pygame.display.update()

    edificio = pygame.image.load("edificio.png")
    pantalla.blit(edificio, (0, 0))
    pygame.display.update()

    fuente = pygame.font.Font(None, 17)  # Se define una fuente

    abierto = True
    while abierto:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                abierto = False
                pygame.quit()

        try:
            datos = next(generador)
            for i in range(1, len(datos)):
                cuarto = datos[i][0]
                anchoi, anchof = dimensiones[cuarto]["ancho"]
                alturai, alturaf = dimensiones[cuarto]["altura"]
                posx = randint(anchoi, anchof)
                posy = randint(alturai, alturaf)
                for x in datos[i][1]:
                    indice = lista.index(x)
                    texto = fuente.render(n_mac[indice], 0, (0, 0, 0), (73, 255, 0))
                    pantalla.blit(texto, (posx, posy))
                    pygame.display.update()
                    clock.tick(FPS)
            pantalla.blit(edificio, (0, 0))
            pygame.display.update()
        except:
            None
    return None


# Tarea 5
def reporte_rango(
    dataset: str,
    cuartos_espol: str,
    inicio: datetime,
    fin: datetime,
) -> None:
    """
    Para un rango específico de horas-minutos, mostrar una animación
    del movimiento (cambio de cuartos) en el edificio para una lista
    de hasta 5 personas (especificadas por el usuario).
    Como respuesta a esta tarea debe adjuntar el video de la animación,
    la misma que debe tener una duración máxima de 1 minuto.
    """
    with open(cuartos_espol) as cuartos_csv:
        next(cuartos_csv)
        dic_cuartos = dict()
        for linea in cuartos_csv:
            nombr_cuarto, aforo, mac1, mac2, mac3 = linea.rstrip().split(",")
            dic_cuartos[str(sorted([mac1, mac2, mac3]))] = (nombr_cuarto, int(aforo))

    with open(dataset) as dt:
        next(dt)

        mismo_segundo = defaultdict(set)
        counter_minuto: Dict = {k: set() for k in dic_cuartos.keys()}

        # Ignorar las lineas previas al inicio solicitado
        try:
            ignorar = True
            while ignorar:
                prim_linea = next(dt)
                segundo_previo = prim_linea[SLICE_TIMESTAMP]
                if int(segundo_previo) >= inicio.timestamp():
                    ignorar = False
            minuto_previo = datetime.fromtimestamp(int(segundo_previo)).minute
            mismo_segundo[prim_linea[SLICE_MAC_CLIENTE]].add(prim_linea[SLICE_MAC_AP])
        except:
            print("Fecha de inicio fuera de registro")
            return None

        dentro_de_rango = True
        while (linea := next(dt, "end")) != "end" and dentro_de_rango:
            if segundo_previo == linea[SLICE_TIMESTAMP]:
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])
            else:
                # Añadimos el número de veces que aparece cada cuarto
                # en el diccionario `mismo_segundo`
                for cliente, macs in mismo_segundo.items():
                    for conjunto_clientes in counter_minuto.values():
                        conjunto_clientes.discard(cliente)
                    counter_minuto[str(sorted(macs))].add(cliente)

                # Liberamos memoria y nos preparamos para la siguiente iteración
                mismo_segundo.clear()
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])

                # Cada que cambia el segundo verificamos si ha pasado un minuto
                timestamp = int(linea[SLICE_TIMESTAMP])
                minuto_actual = datetime.fromtimestamp(timestamp).minute
                if timestamp > fin.timestamp():
                    dentro_de_rango = False
                elif minuto_actual != minuto_previo:
                    minuto_previo = minuto_actual
                    bloque = []
                    bloque.append(
                        datetime.fromtimestamp(int(segundo_previo)).strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    )
                    reporte = {f"c-0{i:02}": (0, "normal") for i in range(1, 11)}
                    for macs_str, clientes in counter_minuto.items():
                        cuarto, aforo_maximo = dic_cuartos[macs_str]
                        if len(clientes) > aforo_maximo:
                            reporte[cuarto] = (len(clientes), "rojo")
                        else:
                            reporte[cuarto] = (len(clientes), "normal")
                    for i in reporte.items():
                        bloque.append(i)
                    yield bloque

                    # reiniciamos el contador de gente y el reporte del minuto
                    for clientes in counter_minuto.values():
                        clientes.clear()
                    reporte.clear()
                    bloque.clear()

            # Al final de cada iteración actualizamos el segundo previo
            segundo_previo = linea[SLICE_TIMESTAMP]

    return None


def alertavista(arch1, arch2, inicio, final):
    fps = 1
    clock1 = pygame.time.Clock()
    pygame.init()
    ANCHO, ALTURA = 1420, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTURA))
    pygame.display.set_caption("Rastreo de personas")
    pygame.display.update()
    x = 0
    y = (ALTURA / 2) - (452 / 2)
    edificio = pygame.image.load("edificio3.png")
    pantalla.blit(edificio, (x, y))
    pygame.display.update()
    pygame.draw.rect(pantalla, (184, 138, 189), [499, 4, 500, 65], 0)
    pygame.display.update()
    fuen = pygame.font.Font(None, 80)
    texto = fuen.render("Tiempo:", 1, [205, 190, 214])
    pantalla.blit(texto, (250, 10))
    pygame.display.update()
    abierto = True
    while abierto:
        generado = reporte_rango(arch1, arch2, inicio, final)
        for info_fechas in generado:
            fecha = info_fechas[0]
            fuen = pygame.font.Font(None, 79)
            pygame.draw.rect(pantalla, (184, 138, 189), [499, 4, 480, 65], 0)
            texto_fecha = fuen.render(fecha, 0, [249, 244, 251])
            pantalla.blit(texto_fecha, (525, 10))
            pygame.display.update()
            posiciones = [
                (50, 142),
                (304, 150),
                (552, 148),
                (101, 383),
                (480, 381),
                (776, 142),
                (1024, 152),
                (1290, 172),
                (831, 375),
                (1202, 370),
            ]
            for e in range(1, 11):
                cuarto1 = info_fechas[e]
                personas, estado = cuarto1[1]
                x = posiciones[e - 1][0]
                y = posiciones[e - 1][1]
                if estado == "rojo":
                    pygame.draw.rect(
                        pantalla, (239, 11, 11), [x - 30, y - 30, 150, 100], 0
                    )
                else:
                    pygame.draw.rect(
                        pantalla, (255, 255, 255), [x - 30, y - 30, 150, 100], 0
                    )
                canti_Personas = fuen.render(str(personas), 0, [0, 0, 0])
                pantalla.blit(canti_Personas, (x + 5, y))
                pygame.display.update()
            clock1.tick(fps)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
    return


# Tarea 6
def tiempo_real(dataset: str, cuartos_espol: str, cuarto: str):
    """
    Dado un cuarto, reporta todos los momentos en los que el cuarto superó
    su aforo máximo, con un mínimo de 10 minutos entre cada alerta.

        Parámetros:
                  dataset (str): Ubicación del log de conexiones
            cuartos_espol (str): Ubicación del archivo csv con el aforo y APs
                                 de cada cuarto
                   cuarto (str): Nombre del cuarto que se desea recibir alertas

        Retorna:
            lista_alertas (list[str]): Lista de los momentos en los que el
                                       cuarto indicado superó su aforo máximo.
            Formato:
                [
                    "AAAA-MM-DD HH:MM, {cantidad} personas",
                    "AAAA-MM-DD HH:MM, {cantidad} personas",
                    ...
                ]
    """
    with open(cuartos_espol) as cuartos_csv:
        next(cuartos_csv)
        for linea in cuartos_csv:
            nombre_cuarto, aforo, mac1, mac2, mac3 = linea.rstrip().split(",")
            if nombre_cuarto == cuarto:
                aforo_max = int(aforo)
                macs_ap = {mac1, mac2, mac3}

    with open(dataset) as dt:
        next(dt)
        mismo_segundo = defaultdict(set)
        disp_presentes = dict()

        # inicializar variables usando la primera linea
        prim_linea = next(dt)
        segundo_previo = prim_linea[SLICE_TIMESTAMP]
        minuto_previo = datetime.fromtimestamp(int(segundo_previo)).minute
        mismo_segundo[prim_linea[SLICE_MAC_CLIENTE]].add(prim_linea[SLICE_MAC_AP])

        for linea in dt:
            if segundo_previo == linea[SLICE_TIMESTAMP]:
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])
            else:
                sleep(0.02)
                # Añadimos el número de dispositivos que hubo en el último segundo
                for cliente, macs in mismo_segundo.items():
                    if macs == macs_ap:
                        disp_presentes[cliente] = linea[SLICE_TIMESTAMP]
                    else:
                        disp_presentes.pop(cliente, "")

                # Liberamos memoria y nos preparamos para la siguiente iteración
                mismo_segundo.clear()
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])

                # Checkeamos aforo cada segundo
                bloque = []
                if len(disp_presentes) >= aforo_max:
                    bloque.append(
                        datetime.fromtimestamp(int(segundo_previo)).strftime("%H:%M")
                    )
                    if len(disp_presentes) == 1:
                        bloque.append(f"{len(disp_presentes)} persona")
                    else:
                        bloque.append(f"{len(disp_presentes)} personas")
                    bloque.append(f"Aforo Máximo: {aforo_max}")
                    bloque.append("rojo")
                    yield bloque
                else:
                    bloque.append(
                        datetime.fromtimestamp(int(segundo_previo)).strftime("%H:%M")
                    )
                    if len(disp_presentes) == 1:
                        bloque.append(f"{len(disp_presentes)} persona")
                    else:
                        bloque.append(f"{len(disp_presentes)} personas")
                    bloque.append(f"Aforo Máximo: {aforo_max}")
                    bloque.append("verde")
                    yield bloque
                bloque.clear()
                # Cada que pasa un minuto reiniciamos estadísticas
                timestamp = int(linea[SLICE_TIMESTAMP])
                minuto_actual = datetime.fromtimestamp(timestamp).minute
                if minuto_actual != minuto_previo:
                    minuto_previo = minuto_actual
                    disp_presentes = {
                        c: t
                        for c, t in disp_presentes.items()
                        if timestamp - int(t) < 5 * 60
                    }

            # Al final de cada iteración actualizamos el segundo previo
            segundo_previo = linea[SLICE_TIMESTAMP]


def alertas_tiempo_real(dataset, cuartos_espol, cuarto):
    # clock = pygame.time.Clock()
    pygame.font.init()
    pygame.mixer.init()

    ANCHO, ALTURA = 500, 500
    VENTANA = pygame.display.set_mode((ANCHO, ALTURA))
    pygame.display.set_caption("Aforo")

    BLANCO = (255, 255, 255)
    VERDE = (0, 255, 0)
    ROJO = (255, 0, 0)
    FUENTE = pygame.font.SysFont("sans-serif", 40)

    run = True
    generador = tiempo_real(dataset, cuartos_espol, cuarto)

    def draw_window(bloque):
        fecha_h, num, aforo, color = bloque
        if color == "verde":
            VENTANA.fill(VERDE)
        else:
            VENTANA.fill(ROJO)
        # tiempo = FUENTE.render(fecha_h, 1, BLANCO)
        numero_personas = FUENTE.render(num, 1, BLANCO)
        aforo_cuarto = FUENTE.render(aforo, 1, BLANCO)
        # VENTANA.blit(tiempo, ((ANCHO - tiempo.get_width()) / 2, ALTURA / 2 - 150))
        VENTANA.blit(
            numero_personas,
            ((ANCHO - numero_personas.get_width()) / 2, ALTURA / 2 - 100),
        )
        VENTANA.blit(
            aforo_cuarto, ((ANCHO - aforo_cuarto.get_width()) / 2, ALTURA / 2 + 100)
        )

        pygame.display.update()

    while run:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window(next(generador))
