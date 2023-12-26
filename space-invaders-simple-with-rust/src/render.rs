use crossterm::{cursor, style, terminal, QueueableCommand};
use std::io::{Stdout, Write};

use crate::frame::Frame;

pub fn render_frame(
    stdout: &mut Stdout,
    last_frame: &Frame,
    current_frame: &Frame,
    force_render: bool, // says if we have to render the entire frame
) {
    if force_render {
        // crossterm's extension "queue" enables us to queue a set of command to the terminal
        stdout
            .queue(style::SetBackgroundColor(style::Color::Blue))
            .unwrap();
        stdout
            .queue(terminal::Clear(terminal::ClearType::All))
            .unwrap(); // clear the whole screen
        stdout
            .queue(style::SetBackgroundColor(style::Color::Black))
            .unwrap();
    }

    for (x_index, column) in current_frame.iter().enumerate() {
        for (y_index, cell_value) in column.iter().enumerate() {
            // cell is of type &&str, so we have to dereference it to get to the value
            if *cell_value != last_frame[x_index][y_index] || force_render {
                stdout
                    .queue(cursor::MoveTo(x_index as u16, y_index as u16))
                    .unwrap();
                print!("{}", cell_value)
            }
        }
    }

    // at the end we will "flush" all commands we queued
    stdout.flush().unwrap();
}
