import base64
from PIL import Image
import numpy as np
import io
from flask import Flask, jsonify, request

from keras.models import load_model

from file_paths import *

# Se carga el modelo
model = load_model(PATH_DEEP_MODEL_SGD)

# Etiquetas de cada clase
labels: dict = {
    'airplane': 0,
    'automobile': 1,
    'bird': 2,
    'cat': 3,
    'deer': 4,
    'dog': 5,
    'frog': 6,
    'horse': 7,
    'ship': 8,
    'truck': 9
}

# Se instancia el servidor y se almacena
# en una variable llamada app.
app = Flask(__name__)

# Tamaño al que se va a ajustar las imagenes
SIZE = (32, 32)

# Ruta del index
@app.route('/')
def index():
    return 'Nothing here...'

# Ruta que recibe una imagen para predecir
@app.route('/predict', methods=['POST'])
def predict():
    # Se valida que se reciba un JSON
    if not request.is_json:
        return jsonify({'message': 'No json received'})
    # Se obtiene la imagen en base64
    image_b64: str = request.get_json().get('image')
    image_b64 = image_b64.split(',')[1]
    # Se valida que el JSON tenga la imagen
    if image_b64 is None:
        return jsonify({'message': 'No image'})
    # Se decodifica la imagen (queda en binario)
    image_b = base64.b64decode(image_b64)
    # Se envia a una funcion para predecir
    class_label = get_prediction(image_b)
    #show_img(image_b)
    #save_img(image_b)
    print(get_key(class_label))
    # Se regresa un JSON que dice si es un perro o no
    return jsonify({'isDog': class_label == labels['dog']})

# Funcion que devuelve el nombre de la etiqueta
def get_key(val: int) -> str:
    for key, value in labels.items():
        if value == val:
            return key
    return 'Class do not exists'

# Funcion que realiza la prediccion de la imagen dada
def get_prediction(image_b: bytes) -> int:
    image = Image.open(io.BytesIO(image_b))\
        .resize(SIZE)
    image_arr = np.array(image)
    image_arr = image_arr.reshape(1, 32, 32, 3)
    y = model.predict(image_arr)[0]
    max_idx = None
    for i in range(len(y)):
        if max_idx is None or y[i] > max_idx:
            max_idx = i
    return max_idx

# Funcion que muestra la imagen recibida en binario
def show_img(image_b: bytes) -> None:
    image = Image.open(io.BytesIO(image_b))\
        .resize(SIZE)
    image.show()

# Funcion que recibe la imagen en base64
# y la almacena en la carpeta img
def save_img(image_b: bytes) -> None:
    with open('img/image.jpg', 'wb') as file:
        file.write(image_b)

# Inicio de la ejecucion
if __name__ == '__main__':
    # Se ejecuta el servidor en modo debug,
    # en el puerto 4000 y abierto a cualquier
    # dispositivo dentro de la red.
    app.run(
        debug=True,
        port=4000,
        host='0.0.0.0'
    )