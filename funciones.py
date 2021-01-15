from datetime import datetime, date, timedelta
from collections import defaultdict, Counter
from typing import Optional, Set, List
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
    inicio_jornada = datetime(anio, mes, dia, 8, 0)
    fin_jornada = datetime(anio, mes, dia, 17, 30)

    with open(dataset) as dt:
        next(dt)
        personas = set()
        for linea in dt:
            mac_cliente = linea[SLICE_MAC_CLIENTE]
            timestamp = int(linea[SLICE_TIMESTAMP])
            fecha_hora = datetime.fromtimestamp(timestamp)
            if inicio_jornada <= fecha_hora <= fin_jornada:
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
                aforo_maximo = int(aforo)
                macs_ap = {mac1, mac2, mac3}

    with open(dataset) as dt:
        next(dt)
        mismo_segundo = defaultdict(set)
        lista_alertas = []
        gente_minuto = 0
        alerta_previa = datetime(1, 1, 1)

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
                gente_minuto += sum(1 for n in mismo_segundo.values() if n == macs_ap)

                # Liberamos memoria y nos preparamos para la siguiente iteración
                mismo_segundo.clear()
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])

                # Cada que cambia el segundo verificamos si ha pasado un minuto
                timestamp = int(linea[SLICE_TIMESTAMP])
                minuto_actual = datetime.fromtimestamp(timestamp).minute
                if minuto_actual != minuto_previo:
                    minuto_previo = minuto_actual
                    fecha_hora = datetime.fromtimestamp(timestamp - 1)
                    if (
                        gente_minuto > aforo_maximo
                        and fecha_hora - alerta_previa > timedelta(minutes=10)
                    ):
                        lista_alertas.append(
                            fecha_hora.strftime("%Y-%m-%d %H:%M")
                            + f", {gente_minuto} personas"
                        )
                        alerta_previa = fecha_hora
                    # reiniciamos el contador de gente
                    gente_minuto = 0

            # Al final de cada iteración actualizamos el segundo previo
            segundo_previo = linea[SLICE_TIMESTAMP]

    return lista_alertas


# Tarea 4
def generar_animacion(dataset: str, cuartos_espol: str, personas: List[str]) -> None:
    """
    Para un rango específico de horas-minutos, mostrar una animación
    del movimiento (cambio de cuartos) en el edificio para una lista
    de hasta 5 personas (especificadas por el usuario).
    Como respuesta a esta tarea debe adjuntar el video de la animación,
    la misma que debe tener una duración máxima de 1 minuto.
    """
    pass


# Tarea 5
def reporte_completo(dataset: str, cuartos_espol: str) -> None:
    """
    Para un rango específico de horas-minutos, mostrar un contador
    minuto a minuto de la cantidad de personas que se encuentra en cada cuarto.
    Si la ocupación supera el aforo máximo del cuarto,
    deberá pintar el cuarto de color rojo.
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
        counter_minuto: ty.Counter[str] = Counter()

        # inicializar variables usando la primera linea
        prim_linea = next(dt)
        segundo_previo = prim_linea[SLICE_TIMESTAMP]
        minuto_previo = datetime.fromtimestamp(int(segundo_previo)).minute
        mismo_segundo[prim_linea[SLICE_MAC_CLIENTE]].add(prim_linea[SLICE_MAC_AP])

        for linea in dt:
            if segundo_previo == linea[SLICE_TIMESTAMP]:
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])
            else:
                # Añadimos el número de veces que aparece cada cuarto
                # en el diccionario `mismo_segundo`
                counter_minuto.update(
                    str(sorted(macs)) for macs in mismo_segundo.values()
                )

                # Liberamos memoria y nos preparamos para la siguiente iteración
                mismo_segundo.clear()
                mismo_segundo[linea[SLICE_MAC_CLIENTE]].add(linea[SLICE_MAC_AP])

                # Cada que cambia el segundo verificamos si ha pasado un minuto
                timestamp = int(linea[SLICE_TIMESTAMP])
                minuto_actual = datetime.fromtimestamp(timestamp).minute
                if minuto_actual != minuto_previo:
                    minuto_previo = minuto_actual
                    print(
                        datetime.fromtimestamp(timestamp - 1).strftime("%Y-%m-%d %H:%M")
                    )
                    reporte = {f"c-0{i:02}": (0, "normal") for i in range(1, 11)}
                    for macs, cantidad in counter_minuto.items():
                        cuarto, aforo_maximo = dic_cuartos[macs]
                        if cantidad > aforo_maximo:
                            reporte[cuarto] = (cantidad, "rojo")
                        else:
                            reporte[cuarto] = (cantidad, "normal")
                    for i in reporte.items():
                        print(i)

                    # reiniciamos el contador de gente y el reporte del minuto
                    counter_minuto.clear()
                    reporte.clear()

            # Al final de cada iteración actualizamos el segundo previo
            segundo_previo = linea[SLICE_TIMESTAMP]

    return None