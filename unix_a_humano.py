from datetime import datetime

with open("logs-conexion.csv") as dt:
    with open("logs-isodate.csv", "w") as f:
        f.write(next(dt))
        for line in dt:
            timestamp = int(line[0:10])
            fecha_hora = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
            f.write(fecha_hora + line[10:])