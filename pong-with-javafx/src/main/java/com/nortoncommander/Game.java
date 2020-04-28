package com.nortoncommander;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.TextAlignment;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.util.Random;

public class Game {
  // Constants
  private static final int STAGE_WIDTH = 1000;
  private static final int STAGE_HEIGHT = 800;
  public static final int PLAYER_WIDTH = 15;
  public static final int PLAYER_HEIGHT = 100;
  public static final int BALL_RADIUS = 15;

  private double ballPositionX = STAGE_WIDTH / 2;
  private double ballPositionY = STAGE_HEIGHT / 2;
  private int ballSpeedX = 1;
  private int ballSpeedY = 1;

  private double playerOnePositionX = 0;
  private double playerOnePositionY = STAGE_HEIGHT / 2;
  private double playerTwoPositionX = STAGE_WIDTH - PLAYER_WIDTH;
  private double playerTwoPositionY = STAGE_HEIGHT / 2;

  private int playerOneScore = 0;
  private int playerTwoScore = 0;

  private boolean hasGameStarted = false;

  private GraphicsContext graphicsContext;

  public Game(Stage stage)  {
    initStage(stage);
  }

  private void initStage(Stage stage) {
    stage.setTitle("P O N G");
    Canvas canvas = createCanvas();
    Scene scene = new Scene(new StackPane(canvas));
    stage.setScene(scene);

    Timeline timeline = new Timeline(new KeyFrame(Duration.millis(10), (event) -> runGame()));
    // define the cycles of our animations
    timeline.setCycleCount(Timeline.INDEFINITE);

    stage.show();
    timeline.play();
  }

  private Canvas createCanvas() {
    final Canvas canvas = new Canvas(STAGE_WIDTH, STAGE_HEIGHT);
    this.graphicsContext = canvas.getGraphicsContext2D();

    // mouse controls
    canvas.setOnMouseMoved((event) -> playerOnePositionY = event.getY());
    canvas.setOnMouseClicked((event) -> hasGameStarted = true);

    return canvas;
  }

  private void runGame() {
    // set background colour
    this.graphicsContext.setFill(Color.BLACK);
    this.graphicsContext.fillRect(0, 0, STAGE_WIDTH, STAGE_HEIGHT);

    // set text colour
    this.graphicsContext.setFill(Color.YELLOW);
    this.graphicsContext.setFont(Font.font(25));

    if (hasGameStarted) {
      startGame();
    } else {
      resetGame();
    }

    // make sure that the ball stays on the canvas
    if (ballPositionY >= STAGE_HEIGHT || ballPositionY <= 0) {
      ballSpeedY *= -1;
    }

    checkIfSomebodyMissedTheBall();

    increaseSpeed();

    // draw the score
    graphicsContext.fillText(playerOneScore + "\t\t\t\t\t\t\t\t\t\t\t\t" + playerTwoScore,
      STAGE_WIDTH / 2, 100);

    // draw the players
    graphicsContext.fillRect(playerOnePositionX, playerOnePositionY, PLAYER_WIDTH, PLAYER_HEIGHT);
    graphicsContext.fillRect(playerTwoPositionX, playerTwoPositionY, PLAYER_WIDTH, PLAYER_HEIGHT);
  }

  private void startGame() {
    // set ball movement
    ballPositionX += ballSpeedX;
    ballPositionY += ballSpeedY;

    // create a simple computer opponent which is following the ball
    if (ballPositionX < STAGE_WIDTH - STAGE_WIDTH / 4) {
      playerTwoPositionY = ballPositionY - PLAYER_HEIGHT / 2;
    } else {
      if (ballPositionY > playerTwoPositionY + PLAYER_HEIGHT / 2) {
        playerTwoPositionY += 1;
      } else {
        playerTwoPositionY -= 1;
      }
    }

    // draw the ball
    graphicsContext.fillOval(ballPositionX, ballPositionY, BALL_RADIUS, BALL_RADIUS);
  }

  private void resetGame() {
    // if game hasn't started yet, show the start text
    this.graphicsContext.setStroke(Color.YELLOW);
    this.graphicsContext.setTextAlign(TextAlignment.CENTER);
    this.graphicsContext.strokeText("Click to start the game", STAGE_WIDTH / 2, STAGE_HEIGHT / 2);

    // reset the ball starting position
    ballPositionY = STAGE_WIDTH / 2;
    ballPositionY = STAGE_HEIGHT / 2;

    // reset the speed and direction of the ball
    ballSpeedX = new Random().nextInt(2) == 0 ? 1 : -1;
    ballSpeedX = new Random().nextInt(2) == 0 ? 1 : -1;
  }

  /**
   * This method is called every time a player hits the ball
   */
  private void increaseSpeed() {
    final boolean ballHitPlayerOne =
      ballPositionX < playerOnePositionX + PLAYER_WIDTH &&
        ballPositionY >= playerOnePositionY &&
        ballPositionY <= playerOnePositionY + PLAYER_HEIGHT;

    final boolean ballHitPlayerTwo =
      ballPositionX + BALL_RADIUS > playerTwoPositionX &&
        ballPositionY >= playerTwoPositionY &&
        ballPositionY <= playerTwoPositionY + PLAYER_HEIGHT;

    if (ballHitPlayerOne || ballHitPlayerTwo) {
      ballSpeedX += 1 * Math.signum(ballSpeedX);
      ballSpeedX *= -1;
      ballSpeedY += 1 * Math.signum(ballSpeedY);
      ballSpeedY *= -1;
    }
  }

  private void checkIfSomebodyMissedTheBall() {
    // computer wins
    if (ballPositionX < playerOnePositionX - PLAYER_WIDTH) {
      playerTwoScore++;
      hasGameStarted = false;
    }

    // user wins
    if (ballPositionX > playerTwoPositionX + PLAYER_WIDTH) {
      playerOneScore++;
      hasGameStarted = false;
    }
  }
}
