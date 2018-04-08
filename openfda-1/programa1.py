#he usado parte del código de un ejercicio realizado en el Laboratorio7 en clase.
import http.client
import json

#la cabecera es un diccionario con una clave y un valor.
#se utiliza para decirle al servidor que tipo de navegador estamos usando.
headers = {'User-Agent': 'http-client'}

#entablamos la conexión con el servidor.
#la funcion HTTPSConnection es del módulo http.client. Con ella podemos entablar conexión con el protocolo https.
llamar_servidor = http.client.HTTPSConnection("api.fda.gov")

#con la función request hacemos una petición de tipo GET al servidor y obtenemos la info del medicamento en formato json.
llamar_servidor.request("GET", "/drug/label.json", None, headers)

#obtenemos respuesta...
respuesta = llamar_servidor.getresponse()

contenido_label = respuesta.read().decode("utf-8")
# gracias a .read podemos leer la info que nos hemos descargado.
# gracias a .decode("utf-8") podemos leer tildes, ñ...
llamar_servidor.close()  # finalizamos la conexión con el servidor.

#a partir de aquí tratamos toda la info(diccionarios y listas mezclados) que hemos obtenido en la respuesta.

label_estructurado = json.loads(contenido_label)
# el load sirve para poderlo indexar con corchetes, sino estaría escrito como un string (lo estructuramos tipo python).
informacion_medicamento = label_estructurado['results'][0]

#imprimimos la info que nos pide el ejerccio.
print (
' ID: ', informacion_medicamento['id'], "\n", 'Proposito: ', informacion_medicamento['purpose'], "\n", 'Fabricante: ',
informacion_medicamento['openfda']['manufacturer_name'])

