package com.nortoncommander;

import javafx.application.Application;
import javafx.stage.Stage;

/**
 * Pong App
 */
public class Pong extends Application {
    @Override
    public void start(Stage stage) {
        new Game(stage);
    }

    public static void main(String[] args) {
        launch();
    }

}
