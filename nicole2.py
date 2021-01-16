from time import time
from datetime import date, datetime
import pandas as pd


def alerta(cuarto):
    data = pd.read_csv("cuartos_espol.csv")
    macs = data.groupby("cuarto")[["mac_ap1", "mac_ap2", "mac_ap3"]].sum()
    dicCuarto = macs.to_dict("index")
    macCuarto = list(dicCuarto[cuarto].values())
    aforo = data.groupby("cuarto").sum().at[cuarto, "aforo_max"]
    logs = open("logs-conexion.csv")
    logs.readline()
    lista_time_mac = []

    dic = {}
    for linea in logs:
        timestamp, mac_ap, mac_cliente = linea.rstrip().split(",")
        if mac_ap in macCuarto:
            dic[timestamp, mac_cliente] = dic.get((timestamp, mac_cliente), []) + [
                mac_ap
            ]
            if len(dic[timestamp, mac_cliente]) == 3:
                lista_time_mac.append((timestamp, mac_cliente))
    dicfechas = {}
    for tiempo, cliente in lista_time_mac:
        unex = int(tiempo)
        fecha = str(datetime.fromtimestamp(unex))
        dicfechas[fecha[:-3]] = dicfechas.get(fecha[:-3], set())
        dicfechas[fecha[:-3]].add(cliente)
    retorno = "REPORTE DEL CUARTO {}\n".format(cuarto)
    fechasCon = []
    for fecha, mcClien in dicfechas.items():
        if len(mcClien) > int(aforo):
            if len(fechasCon) == 0:
                fechasCon.append(fecha)
                retorno += fecha + "," + " " + str(len(mcClien)) + "\n"
            else:
                if int(fecha[-2:]) - int(fechasCon[-1][-2:]) >= 10:
                    fechasCon.append(fecha)
                    retorno += fecha + "," + " " + str(len(mcClien)) + "\n"
    return retorno


t1 = time()
n = alerta("c-010")
t2 = time()
print(n, t2 - t1)
