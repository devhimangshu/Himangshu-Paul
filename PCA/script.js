firebase.initializeApp({
    apiKey: "YOUR_API_KEY",
    authDomain: "your-firebase-project.firebaseapp.com",
    databaseURL: "https://your-firebase-project.firebaseio.com",
    projectId: "your-firebase-project",
    storageBucket: "your-firebase-project.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
});

const database = firebase.database();

document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(err) {
            console.error('Error accessing webcam:', err);
        });

    // Function to send webcam feed to server for face detection
    function detectFaces() {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imgData = canvas.toDataURL('image/jpeg');

        database.ref('/').child('webcam').set(imgData);
    }

    setInterval(detectFaces, 1000); // Adjust the interval as needed
});
