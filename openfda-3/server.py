import http.server
import socketserver
import http.client
import json

#puerto desde donde se lanza el servidor.
PORT = 8000


#creamos una función que devuelva una lista con cada uno de los medicamentos.
#para ello, el programa se tiene que conectar con el servidor.
#nuestra función como cliente lanza una petición de tipo Get
#se recibe una respuesta con información en formato json.
#se trata la iformacion y se estructura.

def dame_lista():
    medicamentos = []

    headers = {'User-Agent': 'http-client'}

    llamar_servidor= http.client.HTTPSConnection("api.fda.gov")
    llamar_servidor.request("GET", "/drug/label.json?limit=10", None, headers)

    respuesta = llamar_servidor.getresponse()
    contenido_label = respuesta.read().decode("utf-8")
    llamar_servidor.close() #finalizamos la conexión con el servidor.

    label_estructurado = json.loads(contenido_label)

#gracias a un bucle for se recorre cada uno de los datos de la informacion y se imprime el nombre genérico.

    for i in range(len(label_estructurado['results'])):
        informacion_medicamento = label_estructurado['results'][i]
        if (informacion_medicamento['openfda']):
            print('Nombre del medicamento: ', informacion_medicamento['openfda']['generic_name'][0])
            medicamentos.append(informacion_medicamento['openfda']['generic_name'][0])
#como hemos usado un editor  json sabemos que un nombre generico de un medicamento no está especificado.
        else:
            medicamentos.append("'Medicamento no especificado'")

 #la función al final devuelve una lista con los 10 medicamentos que se mostrarán mas tarde en el html
    return medicamentos

#clase con herencia.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
#el método GET se invoca automaticamente cada vez que hay una peticion GET por HTTP

    def do_GET(self):
#indicamos OK a la primera linea de la respuesta que es el status.
        self.send_response(200)

# En las siguientes lineas de la respuesta colocamos las cabeceras necesarias para que
# el cliente entienda el tipo de contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
#creamos el html.
        contenido='''<html>
            <body style = "background-color:yellow">
                <h1>Lista de los medicamentos.</h2>
                </body>
                </html>'''

        medicamentos=dame_lista()
        for elemento in medicamentos:
            contenido += '<ul><li>' + elemento + '</li></ul>' + '</br>'

        self.wfile.write(bytes(contenido, "utf8"))
        return



#el servidor comienza a aqui.
#establecemos como manejador nuestra propia clase.
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port"
      "", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()

print("Server stopped!")
