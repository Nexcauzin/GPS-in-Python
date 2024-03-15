import GPS

#COM, BAUD, INDEX, FUSO
setup = GPS.GPS('COM8', 9600, ['Hora', 'Latitude', 'Longitude', 'Altitude'], 3)

setup.leogepas()