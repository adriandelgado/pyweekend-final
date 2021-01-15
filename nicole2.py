from time import time
from datetime import date, datetime
import pandas as pd
def alerta(cuarto):
    data=pd.read_csv('cuartos_espol.csv')
    macs=data.groupby('cuarto')[['mac_ap1','mac_ap2','mac_ap3']].sum()
    dicCuarto= macs.to_dict('index')
    macCuarto=list(dicCuarto[cuarto].values())
    aforo=data.groupby('cuarto').sum().at[cuarto,'aforo_max']
    archivo1 = open('logs-conexion.csv')
    archivo1.readline()
    dic={}
    dicUlti={}
    for linea in archivo1:
        lin=linea.strip().split(',')
        if lin[1] in macCuarto:
            dic[lin[0],lin[-1]]=dic.get((lin[0],lin[-1]),[])+[lin[1]]
            if len(dic[lin[0],lin[-1]])==3:
                dicUlti[lin[0],lin[-1]]=dic[lin[0],lin[-1]]
    dicfechas={}
    for tiempo,cliente in dicUlti:
        unex=int(tiempo)
        fecha = str(datetime.fromtimestamp(unex))
        dicfechas[fecha[:-3]]=dicfechas.get(fecha[:-3],set())
        dicfechas[fecha[:-3]].add(cliente)
    retorno='REPORTE DEL CUARTO {}\n'.format(cuarto)
    fechasCon=[]
    for fecha,mcClien in dicfechas.items():
        if len(mcClien)>int(aforo):
            if len(fechasCon)==0:
                fechasCon.append(fecha)
                retorno += fecha + ',' + ' ' + str(len(mcClien)) + '\n'
            else:
                if (int(fecha[-2:])-int(fechasCon[-1][-2:])>=10):
                    fechasCon.append(fecha)
                    retorno+=fecha+','+' '+str(len(mcClien))+'\n'
    return retorno
t1=time()
n=alerta('c-010')
t2=time()
print(n,t2-t1)


