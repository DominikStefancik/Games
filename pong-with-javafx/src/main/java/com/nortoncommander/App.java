package com.nortoncommander;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
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

import static com.nortoncommander.util.Constants.BALL_RADIUS;
import static com.nortoncommander.util.Constants.PLAYER_HEIGHT;
import static com.nortoncommander.util.Constants.STAGE_HEIGHT;
import static com.nortoncommander.util.Constants.STAGE_WIDTH;

/**
 * JavaFX App
 */
public class App extends Application {

    private double ballPositionX = STAGE_WIDTH / 2;
    private double ballPositionY = STAGE_HEIGHT / 2;
    private int ballSpeedX = 1;
    private int ballSpeedY = 1;

    private int playerOneScore = 0;
    private int playerTwoScore = 0;

    private double playerOnePositionX = 0;
    private double playerOnePositionY = STAGE_HEIGHT / 2;
    private double playerTwoPositionX = 0;
    private double playerTwoPositionY = STAGE_HEIGHT / 2;

    private boolean hasGameStarted = false;

    @Override
    public void start(Stage stage) {
        stage.setTitle("P O N G");
        final Canvas canvas = new Canvas(STAGE_WIDTH, STAGE_HEIGHT);
        GraphicsContext graphicsContext = canvas.getGraphicsContext2D();
        Timeline timeline = new Timeline(new KeyFrame(Duration.millis(10), (event) -> run(graphicsContext)));
        // define the cycles of our animations
        timeline.setCycleCount(Timeline.INDEFINITE);

        // mouse controls
        canvas.setOnMouseMoved((event) -> playerOnePositionY = event.getY());
        canvas.setOnMouseClicked((event) -> hasGameStarted = true);

        Scene scene = new Scene(new StackPane(canvas));
        stage.setScene(scene);
        stage.show();
        timeline.play();
    }

    private void run(GraphicsContext graphicsContext) {
        // set background colour
        graphicsContext.setFill(Color.BLACK);
        graphicsContext.fillRect(0, 0, STAGE_WIDTH, STAGE_HEIGHT);

        // set text colour
        graphicsContext.setFill(Color.YELLOW);
        graphicsContext.setFont(Font.font(25));

        if (hasGameStarted) {
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
        } else {
            resetGame(graphicsContext);
        }

        // make sure that the ball stays on the canvas
        if (ballPositionY >= STAGE_HEIGHT || ballPositionY <= 0) {
            ballSpeedY *= -1;
        }
    }

    private void resetGame(GraphicsContext graphicsContext) {
        // if game hasn't started yet, show the start text
        graphicsContext.setStroke(Color.YELLOW);
        graphicsContext.setTextAlign(TextAlignment.CENTER);
        graphicsContext.strokeText("Click to start the game", STAGE_WIDTH / 2, STAGE_HEIGHT / 2);

        // reset the ball starting position
        ballPositionY = STAGE_WIDTH / 2;
        ballPositionY = STAGE_HEIGHT / 2;

        // reset the speed and direction of the ball
        ballSpeedX = new Random().nextInt(2) == 0 ? 1 : -1;
        ballSpeedX = new Random().nextInt(2) == 0 ? 1 : -1;
    }

    public static void main(String[] args) {
        launch();
    }

}
