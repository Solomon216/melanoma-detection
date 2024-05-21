from flask import Flask, render_template, Response, request, redirect, url_for, send_file
import cv2
import numpy as np
from object_detection_module import realtime  # Replace with the correct import
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

choice = ""
uploaded_image_path = ""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_frames(detection_function):
    source = 0  # Default to webcam
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("Error: Unable to open video source")
        return

    try:
        while True:
            ret = cap.grab()
            if not ret:
                print("Error grabbing frame")
                break

            ret, frame = cap.retrieve()
            if not ret:
                print("Error retrieving frame")
                break

            processed_frame = detection_function(frame)
            _, jpeg_processed = cv2.imencode('.jpg', processed_frame)
            processed_frame_bytes = jpeg_processed.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + processed_frame_bytes + b'\r\n')
    finally:
        cap.release()

def process_image(image_path, detection_function):
    image = cv2.imread(image_path)
    processed_image = detection_function(image)
    _, jpeg_processed = cv2.imencode('.jpg', processed_image)
    return jpeg_processed.tobytes()

@app.route('/', methods=['GET', 'POST'])
def index():
    global choice, uploaded_image_path

    if request.method == 'POST':
        choice = request.form.get('options', '')
        
        if choice == 'Upload' and 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_image_path)
                return redirect(url_for('display_image'))
        elif choice == 'Realtime':
            return redirect(url_for('display_video'))

    return render_template('index.html')

@app.route('/video_feed_processed')
def video_feed_processed():
    global choice
    if choice == "Realtime":
        return Response(generate_frames(realtime),
                        mimetype='multipart/x-mixed-replace; boundary=--frame')
    else:
        return "No valid option selected", 400

@app.route('/display_image')
def display_image():
    global uploaded_image_path
    if uploaded_image_path:
        return render_template('display_image.html')
    else:
        return "No image uploaded", 400
    
@app.route('/display_video')
def display_video():
    global choice
    if choice == "Realtime":
        return render_template('video_feed_processed.html')
    else:
        return "No image uploaded", 400

@app.route('/processed_image')
def processed_image():
    global uploaded_image_path
    if uploaded_image_path:
        processed_image_bytes = process_image(uploaded_image_path, realtime)
        return Response(processed_image_bytes, mimetype='image/jpeg')
    else:
        return "No image uploaded", 400

if __name__ == '__main__':
    app.run(debug=True)
