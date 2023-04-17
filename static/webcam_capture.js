const webcam = document.getElementById("webcam");
const toggleCaptureButton = document.getElementById("toggleCapture");
const resultsDiv = document.getElementById("results");
let captureInterval;
let capturing = false;

navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    webcam.srcObject = stream;
  })
  .catch((err) => {
    console.error(err);
  });

toggleCaptureButton.addEventListener("click", () => {
  capturing = !capturing;
  toggleCaptureButton.textContent = capturing ? "Stop Capture" : "Start Capture";

  if (capturing) {
    captureInterval = setInterval(() => {
      captureFrame(webcam);
    }, 1000); // Capture a frame every 1000ms (1 second)
  } else {
    clearInterval(captureInterval);
  }
});

function captureFrame(videoElement) {
  const canvas = document.createElement("canvas");
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    const formData = new FormData();
    formData.append("image_name", blob, "webcam_frame.jpg");
    fetch("/gender", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Failed to upload frame");
        }
      })
      .then((data) => {
        displayResults(data);
      })
      .catch((error) => {
        console.error(error);
      });
  });
}

function displayResults(data) {
  // TODO: Display the results on the page
  // For now, we just display the raw JSON data
  resultsDiv.innerHTML = JSON.stringify(data, null, 2);
}