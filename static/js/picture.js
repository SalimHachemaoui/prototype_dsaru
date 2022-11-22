let camera_button = document.querySelector("#start-camera");
let stop_button = document.querySelector("#stop-camera");
let webcam = document.querySelector("#webcam");
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");
let img_transform = document.querySelector("#img-transform");
let type = document.getElementById("type");

camera_button.addEventListener("click", async function () {
  let stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false,
  });
  webcam.srcObject = stream;
  window.localStream = stream;
  camera_button.style.display = "none";
  stop_button.style.display = "inline";
});

stop_button.addEventListener("click", function () {
  localStream.getTracks().forEach((track) => {
    track.stop();
  });
  camera_button.style.display = "inline";
  stop_button.style.display = "none";
});

click_button.addEventListener("click", function () {
  canvas.getContext("2d").drawImage(webcam, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(function (blob) {
    var formData = new FormData();
    formData.append(document.getElementById("video-transform").value, blob);
    var requestOptions = {
      method: "POST",
      body: formData,
    };

    fetch("/photo", requestOptions)
      .then((response) => response.blob())
      .then((imageBlob) => {
        var imageObjectURL = URL.createObjectURL(imageBlob);
        img_transform.src = imageObjectURL;
        /*var link = document.createElement("a");
        link.download = "processed_image.png";
        link.href = imageObjectURL;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        delete link;*/
      })
      .catch((error) => console.log("error", error));
  });
});

type.addEventListener("change", function () {
  if (type.value == "photo") {
    document.getElementById("photo-media").style.display = "inline";
    document.getElementById("video-resolution").style.display = "none";
    document.getElementById("video-codec").style.display = "none";
    document.getElementById("stun").style.display = "none";
    document.getElementById("start").style.display = "none";
    document.getElementById("stop").style.display = "none";
  } else {
    stop_button.dispatchEvent(new Event("click"));
    document.getElementById("photo-media").style.display = "none";
    document.getElementById("video-resolution").style.display = "inline";
    document.getElementById("video-codec").style.display = "inline";
    document.getElementById("stun").style.display = "inline";
    document.getElementById("start").style.display = "block";
  }
});
