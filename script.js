const board = document.getElementById("board");
const stage = document.getElementById("stage");
const powerButton = document.getElementById("powerButton");
const resetButton = document.getElementById("resetButton");
const ledButton = document.getElementById("ledButton");

let rotationX = 58;
let rotationZ = -28;
let dragX = 0;
let dragY = 0;
let dragging = false;
let powered = true;
let blinking = false;

document.getElementById("gpio").innerHTML = Array.from({ length: 40 }, () => "<span></span>").join("");

function applyRotation() {
  board.style.transform = `rotateX(${rotationX}deg) rotateZ(${rotationZ}deg)`;
}

stage.addEventListener("pointerdown", (event) => {
  dragging = true;
  dragX = event.clientX;
  dragY = event.clientY;
  stage.setPointerCapture(event.pointerId);
});

stage.addEventListener("pointermove", (event) => {
  if (!dragging) return;
  const deltaX = event.clientX - dragX;
  const deltaY = event.clientY - dragY;
  rotationZ += deltaX * 0.25;
  rotationX = Math.max(25, Math.min(82, rotationX - deltaY * 0.25));
  dragX = event.clientX;
  dragY = event.clientY;
  applyRotation();
});

stage.addEventListener("pointerup", () => { dragging = false; });
stage.addEventListener("pointercancel", () => { dragging = false; });

powerButton.addEventListener("click", () => {
  powered = !powered;
  powerButton.setAttribute("aria-pressed", String(powered));
  powerButton.querySelector("strong").textContent = powered ? "LIGADO" : "DESLIGADO";
  document.querySelectorAll(".led").forEach((led) => led.classList.toggle("off", !powered));
});

resetButton.addEventListener("click", () => {
  rotationX = 58;
  rotationZ = -28;
  applyRotation();
});

ledButton.addEventListener("click", () => {
  blinking = !blinking;
  ledButton.setAttribute("aria-pressed", String(blinking));
  document.querySelectorAll(".led").forEach((led) => led.classList.toggle("blink", blinking && powered));
});
