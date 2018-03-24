#recuperamos el códifo usado en 'programa1.py' y  'programa2.py'.

import http.client
import json


headers = {'User-Agent': 'http-client'}

llamar_servidor = http.client.HTTPSConnection("api.fda.gov")
#el programa puede coger como máximo 100 medicamentos que tengan 'aspirin' entre sus componentes.
#imprimirá por pantalla los 100 primeros que aparezcan.

llamar_servidor.request("GET", '/drug/label.json?limit=100&search=substance_name:"ASPIRIN"', None, headers)
respuesta = llamar_servidor.getresponse()
contenido_label = respuesta.read().decode("utf-8")
llamar_servidor.close() #finalizamos la conexión con el servidor.

label_estructurado = json.loads(contenido_label)


#creamos un bucle que recorra 'results' dentro de la información que nos dan pero estructurada dentro de la variable 'label_estructurado'..
#en la variable 'informacion_medicamento' metemos cada uno de los datos de 'results'.
#imprimimos 'ID' y 'Fabricante' para cada uno de los meddicamentos que recorre e bucle.
for i in range (len (label_estructurado['results'])):
    informacion_medicamento=label_estructurado['results'][i]

    print (' ID: ',informacion_medicamento['id'],"\n",'Fabricante: ', informacion_medicamento['openfda']['manufacturer_name'])