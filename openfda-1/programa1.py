#he usado parte del código de un ejercicio realizado en el Laboratorio7 en clase.
import http.client
import json

#incluyo una cabecera con 'status' y su razón que no se pide que se imprima por pantalla.
#esta información sobre el cliente es útil para estadísticas del propio servidor.
headers = {'User-Agent': 'http-client'}


#entablamos la conexión con el servidor.
llamar_servidor = http.client.HTTPSConnection("api.fda.gov")
#con la función request le pedimos al servidor la informacion contenida en formato json.
llamar_servidor.request("GET", "/drug/label.json", None, headers)
respuesta = llamar_servidor.getresponse()

#obteniendo respuesta del servidor...

contenido_label = respuesta.read().decode("utf-8")
# gracias a .read podemos leer la info que nos hemos descargado.
# gracias a decode poemos leer tildes, ñ...
llamar_servidor.close()  # finalizamos la conexión con el servidor.


label_estructurado = json.loads(contenido_label)
# el load sirve para poderlo indexar con corchetes... sino estaría escrito como un string
informacion_medicamento = label_estructurado['results'][0]
#la variable 'informacion_medicamento' almacena cada uno de los datos que nos ha dado el servidor sobre cada uno de los medicamentos.



#para poder saber como esta estructurado el json he utilizado un editor json, de esta forma podía saber cúal era la información para cada cosa que se pedía.

print (
' ID: ', informacion_medicamento['id'], "\n", 'Proposito: ', informacion_medicamento['purpose'], "\n", 'Fabricante: ',
informacion_medicamento['openfda']['manufacturer_name'])

