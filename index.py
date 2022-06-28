import glob
import io
import os
import uuid
""" 
Si no disponemos de alguna de las librerías que estamos utilizando, 
en este caso numpy, matplotlip procedemos a instalar la librería utilizando 
el comando  
	Pip install matplotlib 
esto funciona cuando se encuentra ubicado en la posición del python
matplotlib nos permite hacer figuras e imprimirlas por medio de un display.
"""
import numpy as np
from flask import Flask, jsonify, make_response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
"""
Se procede a instanciar la clase y ponemos como primer argumento nombre del modulo 
o paquete de la aplicacion esta parte es importante para que flask pueda saber en donde 
buscará recursos como las plantillas templates y archivos estaticos. 

"""
app = Flask(__name__)
app.secret_key = "BONILLA"
app.debug = True
app._static_folder = os.path.abspath("templates/static/")

"""
Route se usa para decirle a flask que url debe activar nuestra función 
es decir devuelve el mensaje que queremos indicar en nuestro navegador. 
El tipo de contenido predeterminado es HTML, por lo que el navegador procesará el HTML de la cadena.
Nos permite dibujar con el maus cualquier imagen para luego obtener una imagen como resultado.

"""
@app.route("/", methods=["GET"])
def index():
    """
    Esta variable nos permite dar un título 
    o un mensaje para que puedan realizar la imagen. 
    Además de crear el fondo con el que vamos a dibujar. 
    """
    title = "Dibuje una imagen"
    return render_template("layouts/index.html", title=title)

"""
En este caso el tipo de contenido predeterminado es acerca de los resultados que obtendremos de la graficación del usuario.
El glob permite encontrar los nombres de rutas que coincidan con un patrón espedífico.
"""
@app.route("/results/", methods=["GET"])
def results():
    title = "Results"
    datalist = []
    for csv in glob.iglob("images/*.csv"):
        datalist.append(get_file_content(csv))
    return render_template("layouts/results.html", title=title, datalist=datalist)

"""
En este caso el tipo de contenido predeterminado es acerca de los resultados que obtendremos de la graficación del usuario.
El método Get lo vamos a utilizar para solicitar datos de un recurso específico. 
"""

@app.route("/results/<unique_id>", methods=["GET"])
def result_for_uuid(unique_id):
    title = "Result"
    data = get_file_content(get_file_name(unique_id))
    return render_template("layouts/result.html", title=title, data=data)

"""
El método de POST envia la información ocultándola de usuarios, 
para usarlo se solicita un servidor web. 
Canvas es un componente, es decir un widget que nos proporciona una superficie en la cual podemos 
trazar elementos tales como líneas, figuras, entre otras.
"""
@app.route("/postmethod", methods=["POST"])
def post_javascript_data():
    jsdata = request.form["canvas_data"]
    unique_id = create_csv(jsdata)
    params = {"unique_id": unique_id}
    return jsonify(params)

"""
Plot es un módulo y sirve para definir la figura que contendrá el gráfico donde vamos a dibujar
para esto se utiliza distintas funciones que dependen del tipo de grafico que se requiera y 
así poder personalizar el gráfico. 
"""
@app.route("/plot/<imgdata>")
def plot(imgdata):
    data = [float(i) for i in imgdata.strip("[]").split(",")]
    data = np.reshape(data, (500, 500))
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.axis("off")
    axis.imshow(data, interpolation="nearest")
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "images/png"
    return response
"""
El UUID es un modulo que proporciona objetos inmutables lo cual nos da una identificación única y el UUID4
nos crea un UUID aleatorio. 
"""

def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open(get_file_name(unique_id), "a") as file:
        file.write(text[1:-1] + "\n")
    return unique_id
"""
La función unique() se usa para encontrar los elementos únicos de una matriz. 
Devuelve los elementos únicos ordenados de una matriz.
"""

def get_file_name(unique_id):
    return f"images/{unique_id}.png"

"""
Get_File_content Devuelve el fichero a un string, y es la mejor manera de 
transmitir el contenido de un fichero a una cadena. De esta manera estamos 
mejorando el rendimiento utilizando técnicas de mapeado. 
"""
def get_file_content(filename):
    with open(filename, "r") as file:
        return file.read()
"""
Aquí definimos un puerto TCP para que nuestra aplicación flask quede con el valor predeterminado es decir 5000. 
Si el puerto es 5000, asumimos que estamos ejecutando la aplicación en nuestra computadora 
y por lo tanto activamos el modo de depuración. 
Al final ejecutamos la aplicación usando host o también conocido como 0.0.0.0
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
