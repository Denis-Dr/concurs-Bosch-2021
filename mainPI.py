import procesare_video_PI as procesare
import time
from flask import Flask, render_template, Response, request
import cv2
import numpy as np

merge = False

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global merge
    #if request.method == "POST":
    if request.form.get("START"):
        merge = True
    elif request.form.get("STOP"):
        merge = False
    return render_template('index.html')
    #elif request.method == "GET":
        #return render_template('index.html')


def gen():
    """Video streaming generator function."""

    global merge
    while merge==True:
        frames = procesare.get_frames_RUNNING()
        for frame in frames:
            _, image = cv2.imencode('.jpeg', frame)
            imgencoded = image.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + imgencoded + b'\r\n')
        procesare.camera.close()

    while merge==False:
        frames = procesare.get_frames_STOPPED()
        for frame in frames:
            _, image = cv2.imencode('.jpeg', frame)
            imgencoded = image.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + imgencoded + b'\r\n')
        procesare.camera.close()


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False, threaded=True)
