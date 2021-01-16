from datetime import datetime
from collections import defaultdict
from typing import Dict, List

SLICE_TIMESTAMP = slice(0, 10)
SLICE_MAC_AP = slice(11, 26)
SLICE_MAC_CLIENTE = slice(27, 42)


# Tarea 4
def generar_datos(
    dataset: str,
    cuartos_espol: str,
    personas: List[str],
    inicio: datetime,
    fin: datetime,
):
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