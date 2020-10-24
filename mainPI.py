import procesare_video_PI as procesare
import time
from flask import Flask, render_template, Response
import cv2
import numpy as np


app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        frames = procesare.get_frames()

        for frame in frames:
            _, image = cv2.imencode('.jpeg', frame)
            imgencoded = image.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + imgencoded + b'\r\n')



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False, threaded=True)