#recuperamos parte del código usado en 'programa1.py' y  'programa2.py'.
import http.client
import json

headers = {'User-Agent': 'http-client'}

#entablamos conexión con el servidor.
llamar_servidor = http.client.HTTPSConnection("api.fda.gov")
num_skip = 0
while True: #bucle infinito.

    #imprimirá por pantalla los 100 primeros que aparezcan(limit).
    #usamos la función skip.
    llamar_servidor.request("GET", '/drug/label.json?limit=100&skip='+ str(num_skip)+'&search=substance_name:"ASPIRIN"', None, headers)
    respuesta = llamar_servidor.getresponse()
    contenido_label = respuesta.read().decode("utf-8")

    label_estructurado = json.loads(contenido_label)

    #imprimimos 'ID' y 'Fabricante' para cada uno de los medicamentos que recorre el bucle.
    for i in range (len (label_estructurado['results'])):
        informacion_medicamento=label_estructurado['results'][i]
        print (' ID: ',informacion_medicamento['id'],'\n','Fabricante: ', informacion_medicamento['openfda']['manufacturer_name'])

    #si de los 100 medicamentos, no todos tienen 'ASPIRIN' el bucle se rompe con un 'break'.
    if len(label_estructurado['results'])<100:
            break

    #si los 100 medicamentos tienen 'ASPIRIN' entonces se saltan los 100 primeros y se continua el bucle.
    num_skip =+100

llamar_servidor.close() #finalizamos la conexión con el servidor.
