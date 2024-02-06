from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
import firebase_admin
from firebase_admin import credentials, db
import face_recognition

# Initialize Firebase
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-project.firebaseio.com'
})

# Load known face encodings from Firebase
known_faces_ref = db.reference('/known_faces')
known_faces = known_faces_ref.get()

app = Flask(__name__)

# Function to recognize faces
def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        for user_id, known_face in known_faces.items():
            matches = face_recognition.compare_faces([known_face['face_encodings']], face_encoding)
            if any(matches):
                name = known_face['name']
                break

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return frame

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for face recognition
@app.route('/detect', methods=['POST'])
def detect_faces():
    # Receive the webcam frame from the client
    image_data = request.form['webcam']
    encoded_data = image_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform face recognition
    frame_with_faces = recognize_faces(frame)

    # Encode the frame with faces and return
    _, buffer = cv2.imencode('.jpg', frame_with_faces)
    response = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'frame': response})

if __name__ == '__main__':
    app.run(debug=True)
