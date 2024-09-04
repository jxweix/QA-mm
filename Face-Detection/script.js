const video = document.getElementById('video');
const modal = document.getElementById('modal');
const welVideo = document.getElementById('welVideo');

let isDetecting = true;
let isPlayingFaceVideo = false;
let isPlayingLoop = false;

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-weights_manifest.json'),
  faceapi.nets.faceLandmark68Net.loadFromUri('https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-weights_manifest.json'),
  faceapi.nets.faceRecognitionNet.loadFromUri('https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-weights_manifest.json'),
  faceapi.nets.faceExpressionNet.loadFromUri('https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_expression_model-weights_manifest.json')
]).then(startVideo);

function startVideo() {
  navigator.mediaDevices.getUserMedia(
    { video: {} }
  ).then(stream => {
    console.log('video streaming', stream);
    video.srcObject = stream;
  }).catch(err => console.error(err));
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    if (isDetecting) {
      const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
      const resizedDetections = faceapi.resizeResults(detections, displaySize);
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
      faceapi.draw.drawDetections(canvas, resizedDetections);
      faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
      faceapi.draw.drawFaceExpressions(canvas, resizedDetections);

      if (resizedDetections.length > 0 && !isPlayingFaceVideo) {
        isDetecting = false; // Stop detection
        isPlayingFaceVideo = true;
        modal.style.display = 'flex';  // Show modal
        welVideo.src = "Wel.mp4";  // Set source to Wel.mp4
        welVideo.loop = false;  // Ensure video doesn't loop
        welVideo.play();  // Play face detection video
      } else if (!isPlayingFaceVideo && !isPlayingLoop) {
        // No face detected, play looping video
        isPlayingLoop = true;
        welVideo.src = "001.mp4";  // Set source to 001.mp4
        welVideo.loop = true;  // Set video to loop
        modal.style.display = 'flex';  // Show modal
        welVideo.play();  // Play looping video
      }
    }
  }, 100);
});

// After Wel.mp4 ends, play 001.mp4 before resuming detection
welVideo.addEventListener('ended', () => {
  if (welVideo.src.includes("Wel.mp4")) {
    // Switch to 001.mp4 after Wel.mp4 finishes
    welVideo.src = "002.mp4";  // Set source to 001.mp4
    welVideo.loop = false;  // Ensure video doesn't loop
    welVideo.play();  // Play 001.mp4
  } else if (welVideo.src.includes("002.mp4")) {
    // Resume detection after 001.mp4 finishes
    modal.style.display = 'none';  // Hide modal
    welVideo.currentTime = 0;  // Reset video to start
    isDetecting = true;  // Resume detection
    isPlayingFaceVideo = false; // Reset flag to allow new detections
    isPlayingLoop = false;  // Reset loop flag
  }
});
