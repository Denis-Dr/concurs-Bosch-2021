import procesare_video_PI as procesare
import time
from flask import Flask, render_template, Response, request
import cv2
import numpy as np

porneste = False

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global porneste
    #if request.method == "POST":
    if request.form.get("START"):
        porneste = True
    elif request.form.get("STOP"):
        porneste = False
    return render_template('index.html')
    #elif request.method == "GET":
        #return render_template('index.html')


def gen():
    """Video streaming generator function."""
    global porneste
    while True:
        frames = procesare.get_frames(porneste)
        # Am putea zice prcesare.get_frames(porneste), unde porneste sa fie true sau false si sa controleze directia;
        # de ex daca porneste==fase atunci trimite comanda viteza zero, iar camera sa transmita in contunuare.
        for frame in frames:
            _, image = cv2.imencode('.jpeg', frame)
            imgencoded = image.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + imgencoded + b'\r\n')


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False, threaded=True)