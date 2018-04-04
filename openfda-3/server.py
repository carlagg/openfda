#recuperamos parte del códico de 'programa1,2,3.py'
import http.server
import socketserver
import http.client
import json

#Puerto desde donde se lanza el servidor.
PORT = 8001



def dame_lista():
    medicamentos = []

    headers = {'User-Agent': 'http-client'}

    llamar_servidor= http.client.HTTPSConnection("api.fda.gov")
    llamar_servidor.request("GET", "/drug/label.json?limit=10", None, headers)

    respuesta = llamar_servidor.getresponse()
    contenido_label = respuesta.read().decode("utf-8")
    llamar_servidor.close() #finalizamos la conexión con el servidor.

    label_estructurado = json.loads(contenido_label)
    for i in range(len(label_estructurado['results'])):
        informacion_medicamento = label_estructurado['results'][i]
        if (informacion_medicamento['openfda']):
            print('Fabricante: ', informacion_medicamento['openfda']['generic_name'][0])
            medicamentos.append(informacion_medicamento['openfda']['generic_name'][0])

    return medicamentos

#clase con herencia.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra en self.path

    def do_GET(self):
        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos lascabeceras necesarias para que el cliente entienda el contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        contenido="<html><body>"
        medicamentos=dame_lista()
        for e in medicamentos:
            contenido += e+"<br>"
        contenido+="</body></html>"

        self.wfile.write(bytes(contenido, "utf8"))
        return



# El servidor comienza a aqui

# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()

print("Server stopped!")
