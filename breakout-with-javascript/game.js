// Game constants
const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 20;
const PADDLE_MARGIN_BOTTOM = 50;
const BALL_RADIUS = 8;
const NUMBER_OF_BRICK_ROWS = 3;
const NUMBER_OF_BRICK_COLUMNS = 5;

let leftArrowPressed = false;
let rightArrowPressed = false;

let lives = 3;

const canvas = document.querySelector("#gameCanvas");
// context of the canvas
const context = canvas.getContext("2d");

// Set the borders of the canvas
canvas.style.border = "1px solid #0ff";
// Make lines stronger when drawing to the canvas
context.lineWidth = 3;

/////// CREATING OBJECTS ///////

// Paddle object
const paddle = {
  x: canvas.width / 2 - PADDLE_WIDTH / 2,
  y: canvas.height - PADDLE_MARGIN_BOTTOM - PADDLE_HEIGHT,
  width: PADDLE_WIDTH,
  height: PADDLE_HEIGHT,
  deltaX: 5,
};

const keyDownHandler = (event) => {
  if (event.key === "ArrowLeft") {
    // user pressed left arrow
    leftArrowPressed = true;
  } else if (event.key === "ArrowRight") {
    // user pressed right arrow
    rightArrowPressed = true;
  }
};

const keyUpHandler = (event) => {
  if (event.key === "ArrowLeft") {
    // user released left arrow
    leftArrowPressed = false;
  } else if (event.key === "ArrowRight") {
    // user released right arrow
    rightArrowPressed = false;
  }
};

// Register listeners for key presses
document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

// Ball object
const ball = {
  x: canvas.width / 2,
  y: paddle.y - BALL_RADIUS,
  radius: BALL_RADIUS,
  speed: 4,
  deltaX: 3 * (Math.random() * 2 - 1),
  deltaY: -3,
};

const brick = {
  width: 55,
  height: 20,
  offsetLeft: 20,
  offsetTop: 20,
  marginTop: 40,
  fillColor: "#2e3548",
  strokeColor: "#FFF",
};

// variable bricksData is an array of arryas of bricks "metadata"
let bricksData;

const setupBricksData = (numberOfRows) => {
  bricksData = [];
  for (let row = 0; row < numberOfRows; row++) {
    const bricksRow = [];
    for (let column = 0; column < NUMBER_OF_BRICK_COLUMNS; column++) {
      const brickSetup = {
        x: column * (brick.offsetLeft + brick.width) + brick.offsetLeft,
        y:
          row * (brick.offsetTop + brick.height) +
          brick.marginTop +
          brick.offsetTop,
        isBroken: false,
      };

      bricksRow.push(brickSetup);
    }

    bricksData.push(bricksRow);
  }
};

/////// DRAWING OBJECTS ///////

const drawPaddle = () => {
  const { x, y, width, height } = paddle;

  context.fillStyle = "#2e3548";
  context.fillRect(x, y, width, height);

  // draw the border of the paddle
  context.strokeStyle = "#ffcd05";
  context.strokeRect(x, y, width, height);
};

const drawBall = () => {
  context.beginPath();

  context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  context.fillStyle = "#ffcd05";
  context.fill();

  // draw the border of the ball
  context.strokeStyle = "#2e3548";
  context.stroke();

  context.closePath();
};

const movePaddle = () => {
  if (leftArrowPressed && paddle.x > 0) {
    paddle.x -= paddle.deltaX;
  }

  if (rightArrowPressed && paddle.x + paddle.width < canvas.width) {
    paddle.x += paddle.deltaX;
  }
};

const moveBall = () => {
  ball.x += ball.deltaX;
  ball.y += ball.deltaY;

  checkBallCollisionWithWall();
  checkBallCollisionWithPaddle();
  checkBallCollisionWithBrick();
};

const checkBallCollisionWithWall = () => {
  if (ball.x - BALL_RADIUS < 0 || ball.x + BALL_RADIUS > canvas.width) {
    ball.deltaX *= -1;
  }

  if (ball.y - BALL_RADIUS < 0) {
    ball.deltaY *= -1;
  } else if (ball.y + BALL_RADIUS > canvas.height) {
    lives--;
    resetBall();
  }
};

const checkBallCollisionWithPaddle = () => {
  const ballIsOnPaddleHorizontally =
    ball.x > paddle.x && ball.x < paddle.x + PADDLE_WIDTH;
  const ballIsOnPaddleVertically = ball.y + BALL_RADIUS > paddle.y;

  if (ballIsOnPaddleHorizontally && ballIsOnPaddleVertically) {
    let collidePoint = ball.x - paddle.x - PADDLE_WIDTH / 2;

    // Normalise the values
    collidePoint = collidePoint / (PADDLE_WIDTH - 2);

    // Calculate the angle of the ball
    const angle = (collidePoint * Math.PI) / 3;

    ball.deltaX = ball.speed * Math.sin(angle);
    ball.deltaY = -ball.speed * Math.cos(angle);
  }
};

const checkBallCollisionWithBrick = () => {
  for (let row = 0; row < bricksData.length; row++) {
    const bricksRow = bricksData[row];
    let isBrickHit = false;
    for (let column = 0; column < bricksRow.length; column++) {
      const brickMetadata = bricksRow[column];
      // the brick is still visible on the canvas
      if (!brickMetadata.isBroken) {
        const ballHitBrickOnBottom =
          ball.y - BALL_RADIUS < brickMetadata.y + brick.height;
        const ballHitBrickOnTop =
          ball.y - BALL_RADIUS < brickMetadata.y &&
          ball.y + BALL_RADIUS > brickMetadata.y;
        const ballHitBrickLength =
          ball.x > brickMetadata.x && ball.x < brickMetadata.x + brick.width;

        if ((ballHitBrickOnBottom || ballHitBrickOnTop) && ballHitBrickLength) {
          brickMetadata.isBroken = true;
          ball.deltaY *= -1;
          isBrickHit = true;
          break;
        }
      }
    }
  }
};

const resetBall = () => {
  ball.x = canvas.width / 2;
  ball.y = paddle.y - BALL_RADIUS;
  ball.speed = 4;
  ball.deltaX = 3 * (Math.random() * 2 - 1);
  ball.deltaY = -3;
};

const drawBrick = (x, y) => {
  context.fillStyle = brick.fillColor;
  context.fillRect(x, y, brick.width, brick.height);

  // draw the border of the brick
  context.strokeStyle = brick.strokeColor;
  context.strokeRect(x, y, brick.width, brick.height);
};

const drawBricks = () => {
  for (let row = 0; row < bricksData.length; row++) {
    const bricksRow = bricksData[row];
    for (let column = 0; column < bricksRow.length; column++) {
      const data = bricksRow[column];
      if (!data.isBroken) {
        drawBrick(data.x, data.y);
      }
    }
  }
};

// Draws the content if the canvas
const drawCanvasContent = () => {
  drawPaddle();
  drawBall();
  drawBricks();
};

const updateCanvas = () => {
  movePaddle();
  moveBall();
};

const gameLoop = () => {
  context.drawImage(BACKGROUND_IMAGE, 0, 0);

  drawCanvasContent();
  updateCanvas();

  window.requestAnimationFrame(gameLoop);
};

// before we start the game loop, we initialise bricks
setupBricksData(NUMBER_OF_BRICK_ROWS);
gameLoop();
