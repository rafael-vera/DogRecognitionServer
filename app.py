import base64
from flask import Flask, jsonify, request

# Se instancia el servidor y se almacena
# en una variable llamada app.
app = Flask(__name__)

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
    # Se valida que el JSON tenga la imagen
    if image_b64 is None:
        return jsonify({'message': 'No image'})
    # Se decodifica la imagen (queda en binario)
    save_img(image_b64)
    # Se envia a una funcion para predecir
    # Se muestra la imagen condificada en base64
    return f'<img src="data:image/png;base64,{image_b64}">'

# Funcion que recibe la imagen en base64
# y la almacena en la carpeta img
def save_img(image_b64) -> None:
    with open('img/image.jpg', 'wb') as file:
        file.write(base64.b64decode(image_b64))

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