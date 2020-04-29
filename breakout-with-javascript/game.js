// Game constants
const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 20;
const PADDLE_MARGIN_BOTTOM = 50;

const canvas = document.querySelector("#gameCanvas");
// context of the canvas
const context = canvas.getContext("2d");

// Set the borders of the canvas
canvas.style.border = "1px solid #0ff";
// Make lines stronger when drawing to the canvas
context.lineWidth = 3;

// Paddle object
const paddle = {
  x: canvas.width / 2 - PADDLE_WIDTH / 2,
  y: canvas.height - PADDLE_MARGIN_BOTTOM - PADDLE_HEIGHT,
  width: PADDLE_WIDTH,
  height: PADDLE_HEIGHT,
  deltaX: 5,
};

const drawPaddle = () => {
  const { x, y, width, height } = paddle;

  context.fillStyle = "#2e3548";
  context.fillRect(x, y, width, height);

  // draw the border of the paddle
  context.strokeStyle = "#ffcd05";
  context.strokeRect(x, y, width, height);
};

// Draws the content if the canvas
const drawCanvasContent = () => {
  drawPaddle();
};

const gameLoop = () => {
  context.drawImage(BACKGROUND_IMAGE, 0, 0);

  drawCanvasContent();

  window.requestAnimationFrame(gameLoop);
};

gameLoop();
