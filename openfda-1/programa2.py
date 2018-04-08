#recuperamos el código del 'programa1.py'

import http.client
import json

headers = {'User-Agent': 'http-client'}

llamar_servidor = http.client.HTTPSConnection("api.fda.gov")

#ponemos el limite en 10 porque queremos saber el ID de los primeros 1os medicamentos.
#esto se incluye dentro del recurso.
llamar_servidor.request("GET", "/drug/label.json?limit=10", None, headers)

respuesta = llamar_servidor.getresponse()
contenido_labeĺ = respuesta.read().decode("utf-8")
llamar_servidor.close() #fianlizmos la conexón con el servidor.
label_estructurado = json.loads(contenido_labeĺ)

#creamos un bucle que recorra toda la longitud del contenido de la respuesta pero ya estructurada.
#sólo en los datos dentro de 'results'.
for i in range (len (label_estructurado['results'])):
    informacion_medicamento=label_estructurado['results'][i]

    #dentro de la info de 'results' hay una lista con el id.
    print ('ID: ',informacion_medicamento['id'])
