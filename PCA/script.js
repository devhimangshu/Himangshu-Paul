document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
        video.srcObject = stream;
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
});
