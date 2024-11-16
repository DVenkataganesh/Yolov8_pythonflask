from flask import Flask, render_template, request, Response, url_for
import cv2
from ultralytics import YOLO
import urllib.request
import numpy as np
import os

app = Flask(__name__)

# Load YOLO model
model = YOLO("best.pt")

# Initialize the video capture
camera = None

# Directory to save uploaded images
STATIC_FOLDER = 'static'
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

def generate_frames():
    """Generate frames from the camera."""
    global camera
    if camera is None:
        return

    # Define your custom confidence threshold here (e.g., 30%)
    conf_threshold = 0.3  # Reduced threshold for detections

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Perform detection with the reduced confidence threshold
            results = model(frame, conf=conf_threshold)  # Adjusting confidence threshold
            frame = results[0].plot()  # Annotate detections on the frame

            # Convert the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame for live preview
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    global camera
    if camera is None:
        return "Camera is off", 404
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_camera', methods=['POST'])
def toggle_camera():
    """Turn the camera on or off."""
    global camera
    action = request.form.get('action')
    if action == "on":
        if camera is None:
            camera = cv2.VideoCapture(0)
    elif action == "off":
        if camera is not None:
            camera.release()
            camera = None
    return ("", 204)

@app.route('/detect', methods=['POST'])
def detect():
    """Detect objects in an uploaded image or image from a URL."""
    file = request.files.get('file')
    image_url = request.form.get('image_url')

    if file:
        # Save and read the uploaded file
        filepath = os.path.join(STATIC_FOLDER, file.filename)
        file.save(filepath)
        image = cv2.imread(filepath)
    elif image_url:
        # Fetch the image from the URL
        resp = urllib.request.urlopen(image_url)
        image_array = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    else:
        return "No image provided!", 400

    # Define your custom confidence threshold here (e.g., 30%)
    conf_threshold = 0.3  # Reduced threshold for detections

    # Perform detection with the reduced confidence threshold
    results = model(image, conf=conf_threshold)
    annotated_image = results[0].plot()  # Annotate detections

    # Save the annotated image in the static folder
    output_path = os.path.join(STATIC_FOLDER, "output.jpg")
    cv2.imwrite(output_path, annotated_image)

    return render_template('result.html', image_path="output.jpg")

if __name__ == '__main__':
    app.run(debug=True)
