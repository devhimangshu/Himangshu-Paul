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

    let stream = null;

    // Function to access webcam
    async function startWebcam() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            console.error('Error accessing webcam:', err);
        }
    }

    // Function to send webcam feed to server for face detection
    function detectFaces() {
        if (!stream) return; // Don't proceed if webcam is not started

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imgData = canvas.toDataURL('image/jpeg');

        database.ref('/').child('webcam').set(imgData);
    }

    // Event listener for the start button
    document.getElementById('startButton').addEventListener('click', startWebcam);

    setInterval(detectFaces, 1000); // Adjust the interval as needed
});
