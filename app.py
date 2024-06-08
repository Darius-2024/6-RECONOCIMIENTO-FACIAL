from flask import Flask, render_template, Response, jsonify, request
from flask_sslify import SSLify
from reconocimientoFacial import gen_frames
from capturandoRostros import gen_frames_capture
from entrenandoRF import run_entrenamiento
from datos import obtener_personas_reconocidas

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capturar')
def capturar():
    return render_template('capturar.html')

@app.route('/reconocer')
def reconocer():
    return render_template('reconocer.html')

@app.route('/listar')
def listar():
    return render_template('listar.html')

@app.route('/obtener_reconocidas')
def obtener_reconocidas():
    personas = obtener_personas_reconocidas()
    return personas

@app.route('/video_feed')
def video_feed():
    latitud = request.args.get('latitud')
    longitud = request.args.get('longitud')
    return Response(gen_frames(latitud, longitud), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_captura')
def video_feed_captura():
    document = request.args.get('documento')
    nrofotos = request.args.get('nrofotos')
    return Response(gen_frames_capture(document, nrofotos), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/entrenamiento')
def entrenamiento():
    return Response(run_entrenamiento(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=8081, host="0.0.0.0", ssl_context='adhoc')
    #app.run(debug=True, port=8081, host="0.0.0.0")
