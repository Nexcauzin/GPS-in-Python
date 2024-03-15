import serial
from datetime import datetime, timedelta

class GPS:
    def __init__(self, nome, porta, baud, colunas, fuso):
        self.nome = nome
        self.porta = porta
        self.baud = baud
        self.colunas = colunas
        self.fuso = fuso

    def converte_horario(self, time):
        time = datetime.strptime(time, "%H%M%S.%f")
        tempo_fuso = time - timedelta(self.fuso)
        if(tempo_fuso.month > 2 and tempo_fuso.month < 10) or (tempo_fuso.month == 2 and tempo_fuso.day < 20 and tempo_fuso.weekday() == 6) or (tempo_fuso.month == 10 and tempo_fuso.day > 20 and tempo_fuso.weekday() == 6):
            tempo_fuso = tempo_fuso + timedelta(hours=1)
        return tempo_fuso.strftime("%H:%M:%S")
    
    def leogepas(self):
        with serial.Serial(self.porta, self.baud, timeout=1) as ser:
            while True:
                leitura = ser.readline().decode('utf-8').strip()
                if leitura.startswith('$GPGGA'):
                    dados = leitura.split(',')
                    if len(dados) >= 15:
                        graus_latitude = str(dados[2])
                        dir_latitude = dados[3]
                        latitude = int(graus_latitude[:2] + float(graus_latitude[2:])/60)
                        if dir_latitude == 'S':
                            latitude = -latitude
                        
                        graus_longitude = str(dados[4])
                        dir_longitude = dados[5]
                        longitude = int(graus_longitude[:3]) + float(graus_longitude[3:])/60
                        if dir_longitude == 'W':
                            longitude = -longitude
                        
                        altitude = dados[9] # analisar se coloca altura tmb

                        hora = self.converte_horario(dados[1])
                        gps = [hora, latitude, longitude, altitude]
                        #Aqui implementa a questão do firebase/mapa em tempo real
                        