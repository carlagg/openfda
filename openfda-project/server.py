import http.server
import http.client
import socketserver
import json


PORT=8000

#Se crea una clase que herede a otra.
#El metodo que está programado sólo responde al do_get.
#define el comportamiento de lo que tenemos que hacer ante un http.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    #Se crea la primera función auxiliar.
    #Nos devulve el contenido html que aparecerá cuando se ejecute el programa.
    def get_html(self):
        #Se define el contenido html.
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body style="background-color: #00ed8d">
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    -
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                   -
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    -
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    -
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        #Se devulve el contenido html.
        return html

    #Creamos la segunda función auxiliar.
    def dame_resultados (self, limit=10):
        llamar_servidor = http.client.HTTPSConnection("api.fda.gov")
        llamar_servidor.request("GET", "/drug/label.json" + "?limit="+str(limit))
        print ("/drug/label.json" + "?limit="+str(limit))
        respuesta = llamar_servidor.getresponse()
        contenido_datos = respuesta.read().decode("utf8")
        datos_estructurados = json.loads(contenido_datos)
        resultados = datos_estructurados['results']
        return resultados

    #Se crea la tercera función auxiliar.
    #Recibe una lista de informacion y genera una pagina html con los ul li barra li. (depende la ifo del recurso)
    def dame_web (self, lista):
        #lista_html almacena cada lista de información pero en contenido html.
        lista_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        #Bucle que va iterando e implementando los datos de las listas que puede leer el programa.
        for i in lista:
            lista_html += "<li>" + i + "</li>"

        #Se añaden al html.
        lista_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return lista_html
        #Devuelve el contenido html.

    #El método que se crea a continuación es el único que se ejecuta de entrada.
    #Puede llamar a los tres métodos auxiliares anteriores para realizar las tareas.
    def do_GET(self):

        #La variable self.path puede valer cosas como los recursos (listcompanies?limit=10).
        recurso_list = self.path.split("?")
        # recurso_list, tiene dos elementos con dos posiciones por donde se ha hecho el split.

        #Si después de la interrogación hay algo escrito entonces la posicion 1 de la lista serán los parametros.
        if len(recurso_list) > 1:
            parametros = recurso_list[1]
        else:
            parametros = ""

        #Aquí especificamos el número de resultasdos que van a aparecer en el navegador por defecto.
        limit = 1

        # Obtener los parametros.
        #Si hay parametros limit =10.
        if parametros:

            #Se divide el recurso y el parametro por el "=".
            parse_limit = parametros.split("=")

            #Detectamos de esta forma el parametro limit (limitacion).
            if parse_limit[0] == "limit":

                limit = int(parse_limit[1])
                #La segunda posicion es un numero int.(lo cambiamos de str).

                print("Limit: {}".format(limit))

        else:
            print("SIN PARAMETROS")

        #Escribimos el contenido como utf-8 data.
        #Es el único recurso que no puede tener parámetros (no existe /?limit=10).
        if self.path=='/':

            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')#cabecera de texto html.
            self.end_headers()

            html=self.get_html()
            #Llama al primer método que hemos creado.
            #Construye la web de los formularios como un str y me lo devuelve.
            #La web tiene el html que hay que devolver al usuario.

            self.wfile.write(bytes(html, "utf8"))
        elif 'searchDrug' in self.path:
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #Por defecto 10 en este caso, no 1
            limit = 10
            drug=self.path.split('=')[1]


            #Creamos una lista vacía a la cúal se irán añadiendo datos que iteren en el bucle for.
            #Llamamos al servidor, obtenemos los resultados y los metemos en la lista.
            lista_drugs = []
            llamar_servidor = http.client.HTTPSConnection("api.fda.gov")
            llamar_servidor.request("GET","/drug/label.json"+"?limit="+str(limit)+'&search=active_ingredient:'+drug)
            respuesta = llamar_servidor.getresponse()
            datos = respuesta.read()
            datos_estructurados = datos.decode("utf8")
            biblioteca_datos = json.loads(datos_estructurados)
            events_search_drug = biblioteca_datos['results']
            for resultado in events_search_drug:
                if ('generic_name' in resultado['openfda']):
                    lista_drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    lista_drugs.append('Fármaco desconocido.')

            #Todos los datos obtenidos crearan una web gracias al método que creamos.
            resultado_html = self.dame_web(lista_drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))
            #Se devolverán al cliente como contenido html.
        elif 'searchCompany' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #En este caso tienen que aparecer por defecto 10.
            limit = 10

            #La forma de sacar la iformación de openfda y devolverla como contenido html es la misma que en el caso anterior.
            company=self.path.split('=')[1]
            lista_companies = []
            llamar_servidor = http.client.HTTPSConnection("api.fda.gov")
            llamar_servidor.request("GET","/drug/label.json"+"?limit="+str(limit)+'&search=openfda.manufacturer_name:'+company)
            respuesta = llamar_servidor.getresponse()
            datos = respuesta.read()
            datos_estructurados = datos.decode("utf8")
            biblioteca_datos = json.loads(datos_estructurados)
            events_search_company = biblioteca_datos['results']

            for event in events_search_company:
                lista_companies.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.dame_web(lista_companies)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_medicamentos = []
            resultados = self.dame_resultados(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    lista_medicamentos.append (resultado['openfda']['generic_name'][0])
                else:
                    lista_medicamentos.append('Medicamento desconocido.')
            resultado_html = self.dame_web (lista_medicamentos)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listCompanies' in self.path:
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            lista_companies = []
            resultados = self.dame_resultados(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    lista_companies.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    lista_companies.append('Compañía desconocida.')
            resultado_html = self.dame_web(lista_companies)

            self.wfile.write(bytes(resultado_html, "utf8"))


        #Extensión I referida a las advertencias de los fármacos.
        elif 'listWarnings' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #La información se obtiene de la misma forma que en los casos anteriores.
            lista_warnings = []
            resultados = self.dame_resultados(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    lista_warnings.append (resultado['warnings'][0])
                else:
                    lista_warnings.append('Desconocido')
            resultado_html = self.dame_web(lista_warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))

        #Extensión IV referida a redirección y autenticación.
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        elif 'redirect' in self.path:
            print("Redirección a la página principal")
            self.send_response(301)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()

        #Extensión II referida al Error 404 para aquellos recursos no encontrados.
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return

#Aquí es donde se empieza a ejecutar el programa.
#Va haciendo caso a las peticiones que le haga el cliente.

#Para no tener que estar cambiando el puerto donde escucha el servidor cada vez que cerramos.
#El enunciado de la práctica nos pide poner la siguiente línea.
socketserver.TCPServer.allow_reuse_address= True

Handler = testHTTPRequestHandler
#Es la instancia de una clase.
#Se encarga de atender a las peticiones http que puedan llegar desde dos puntos:
#un navegador que se conecte de forma manual y directa, o el propio test que nos han dado  de la practica.

httpd = socketserver.TCPServer(("", PORT), Handler)
#Asocia una ip y un puerto a nuestro manejador de peticiones.
#Cuando nos llegue una peticion a la ip y al puerto , el programa le dice a nuestro manejador que la atienda.

print("serving at port", PORT)

httpd.serve_forever()
#Ejecuta el server para siempre