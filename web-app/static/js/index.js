const video = document.getElementById("camera");
const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const message = document.getElementById("message");
const list = document.getElementById("predictions");
const result = document.getElementById("result");
const seedButton = document.getElementById("seedBtn");

const canvas = document.createElement("canvas");

let stream = null;

startButton.addEventListener("click", async () => {
  startButton.disabled = true;
  message.textContent = "";

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 400, height: 400 },
      audio: false,
    });

    video.srcObject = stream;
    stopButton.disabled = false;
  } catch (error) {
    message.textContent = `Could not access camera: ${error.message}`;
    startButton.disabled = false;
  }
});

stopButton.addEventListener("click", () => {
  stream?.getTracks().forEach((track) => track.stop());
  stream = null;
  video.srcObject = null;

  startButton.disabled = false;
  stopButton.disabled = true;
});

setInterval(() => {
  if (!stream) return;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);

  canvas.toBlob(async (blob) => {
    const form = new FormData();
    form.append("frame", blob, "frame.jpg");

    const response = await fetch("/api/frame", { method: "POST", body: form });

    const data = await response.json();
    document.getElementById("result").textContent = data.text;
  }, "image/jpeg");
}, 1000);

async function refreshLetters() {
  const response = await fetch("/api/predictions");
  const letters = await response.json();

  list.replaceChildren();

  if (letters.length === 0) {
    const item = document.createElement("li");
    item.textContent = "No letters yet.";
    list.appendChild(item);
    return;
  }

  for (const letter of letters) {
    const percent = Math.round(letter.confidence * 100);
    const item = document.createElement("li");
    const label = document.createElement("strong");

    label.textContent = letter.letter;
    item.append(label, ` (${percent}%)`);
    list.appendChild(item);
  }
}

document.getElementById("seedBtn").onclick = async () => {
  await fetch("/api/seed", { method: "POST" });
  await refreshLetters();
};
