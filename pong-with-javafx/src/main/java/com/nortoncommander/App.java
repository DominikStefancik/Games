package com.nortoncommander;

import javafx.application.Application;
import javafx.stage.Stage;

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

        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }

}
