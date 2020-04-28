package com.nortoncommander;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
import javafx.util.Duration;


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
        stage.show();
        timeline.play();
    }

    private void run(GraphicsContext graphicsContext) {

    }

    public static void main(String[] args) {
        launch();
    }

}
