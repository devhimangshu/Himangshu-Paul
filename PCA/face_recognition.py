import cv2
import face_recognition
import requests

# Function to recognize faces
def recognize_faces(frame):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Call your face identification API to identify the person
        person_name = identify_person(rgb_frame[top:bottom, left:right])
        
        # Draw text label with person's name
        cv2.putText(frame, person_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

# Function to call the face identification API
def identify_person(face_image):
    # Example: Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
    api_endpoint = 'https://example.com/identify'
    
    # Example: Replace 'YOUR_API_KEY' with your actual API key (if required)
    api_key = 'YOUR_API_KEY'
    
    # Example: Construct the request payload (image data and API key)
    payload = {'image': face_image, 'api_key': api_key}
    
    try:
        # Example: Make a POST request to the API
        response = requests.post(api_endpoint, data=payload)
        
        # Example: Extract the person's name from the API response
        person_name = response.json().get('name', 'Unknown')
        
        return person_name
    except Exception as e:
        print("Error calling face identification API:", e)
        return 'Unknown'

# Main function
def main():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        frame = recognize_faces(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
