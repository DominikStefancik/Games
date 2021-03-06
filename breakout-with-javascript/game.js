// Game constants
const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 20;
const PADDLE_MARGIN_BOTTOM = 50;
const BALL_RADIUS = 8;
const NUMBER_OF_BRICK_ROWS = 3;
const NUMBER_OF_BRICK_COLUMNS = 5;
const STATISTICS_OFFSET = 25;
const BRICK_SCORE = 10;
const MAX_LEVEL = 6;

let leftArrowPressed = false;
let rightArrowPressed = false;

let score = 0;
let level = 1;
let lives = 3;

let isGameOver = false;
let isGameWon = false;
let isNextLevel = false;
let isSoundMuted = false;

const canvas = document.querySelector("#gameCanvas");
// context of the canvas
const context = canvas.getContext("2d");

// Set the borders of the canvas
canvas.style.border = "1px solid #0ff";
// Make lines stronger when drawing to the canvas
context.lineWidth = 3;

const levelUpTheGame = () => {
  playSound(WIN_AUDIO);
  level++;
  isGameWon = isGameOver = level > MAX_LEVEL;
  isNextLevel = !isGameWon; // the game is not won yet, we can go to the next level
  ball.speed *= 0.5;
};

const playSound = (sound) => {
  if (!isSoundMuted) {
    sound.play();
  }
};

const toggleSound = (event) => {
  if (event.key === "m" || event.key === "M") {
    isSoundMuted = !isSoundMuted;
  }
};

// add a listener for muting/unmuting sound effects
document.addEventListener("keypress", toggleSound);

/////// CREATING OBJECTS ///////

const soundImage = {
  width: 30,
  height: 30,
  top: 460,
  left: 10,
};

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

// the number of rows changes each level
const setupBricksData = () => {
  bricksData = [];
  for (let row = 0; row < NUMBER_OF_BRICK_ROWS + level - 1; row++) {
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

const areAllBricksBroken = () => {
  for (let row = 0; row < bricksData.length; row++) {
    const bricksRow = bricksData[row];
    for (let column = 0; column < bricksRow.length; column++) {
      const brickMetadata = bricksRow[column];
      if (!brickMetadata.isBroken) {
        return false;
      }
    }
  }

  return true;
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

const resetPaddle = () => {
  paddle.x = canvas.width / 2 - PADDLE_WIDTH / 2;
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
    playSound(WALL_HIT_AUDIO);
    ball.deltaX *= -1;
  }

  if (ball.y - BALL_RADIUS < 0) {
    playSound(WALL_HIT_AUDIO);
    ball.deltaY *= -1;
  } else if (ball.y + BALL_RADIUS > canvas.height) {
    playSound(LIFE_LOST_AUDIO);
    lives--;

    if (lives === 0) {
      isGameOver = true;
      isGameWon = false;
    } else {
      resetBall();
    }
  }
};

const checkBallCollisionWithPaddle = () => {
  const ballIsOnPaddleHorizontally =
    ball.x > paddle.x && ball.x < paddle.x + PADDLE_WIDTH;
  const ballIsOnPaddleVertically = ball.y + BALL_RADIUS > paddle.y;

  if (ballIsOnPaddleHorizontally && ballIsOnPaddleVertically) {
    playSound(PADDLE_HIT_AUDIO);
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
          playSound(BRICK_HIT_AUDIO);
          brickMetadata.isBroken = true;
          score += BRICK_SCORE;
          if (areAllBricksBroken()) {
            levelUpTheGame();
          } else {
            ball.deltaY *= -1;
          }

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

const showGameStatistics = (
  text,
  textX,
  textY,
  image,
  imageX,
  imageY,
  imageWidth,
  imageHeight
) => {
  context.fillStyle = "#FFF";
  context.font = "25px Germania One";
  context.fillText(text, textX, textY);
  context.drawImage(image, imageX, imageY, imageWidth, imageHeight);
};

const showGameOverImage = () => {
  if (isGameWon) {
    context.drawImage(
      GAME_WON_IMAGE,
      100,
      canvas.height / 2 - 70,
      canvas.width - 200,
      150
    );
  } else {
    context.drawImage(
      GAME_LOST_IMAGE,
      0,
      canvas.height / 2 - 150,
      canvas.width,
      300
    );
  }
};

// Draws the content if the canvas
const drawCanvasContent = () => {
  context.drawImage(BACKGROUND_IMAGE, 0, 0);
  showGameStatistics(
    score,
    35,
    STATISTICS_OFFSET,
    SCORE_IMAGE,
    5,
    5,
    STATISTICS_OFFSET,
    STATISTICS_OFFSET
  );
  showGameStatistics(
    level,
    canvas.width / 2,
    STATISTICS_OFFSET,
    LEVEL_IMAGE,
    canvas.width / 2 - 30,
    5,
    STATISTICS_OFFSET,
    STATISTICS_OFFSET
  );
  showGameStatistics(
    lives,
    canvas.width - 25,
    STATISTICS_OFFSET,
    LIFE_IMAGE,
    canvas.width - 65,
    -5,
    45,
    45
  );

  drawPaddle();
  drawBall();
  drawBricks();

  context.drawImage(
    isSoundMuted ? SOUND_OFF_IMAGE : SOUND_ON_IMAGE,
    soundImage.left,
    soundImage.top,
    soundImage.width,
    soundImage.height
  );
};

const updateCanvas = () => {
  movePaddle();
  moveBall();

  if (isNextLevel) {
    resetCanvas();
    isNextLevel = false;
  }
};

const resetCanvas = () => {
  setupBricksData();
  resetPaddle();
  resetBall();
};

const gameLoop = () => {
  drawCanvasContent();
  updateCanvas();

  if (!isGameOver) {
    window.requestAnimationFrame(gameLoop);
  } else {
    showGameOverImage();
  }
};

// before we start the game loop, we initialise bricks
setupBricksData();
gameLoop();
