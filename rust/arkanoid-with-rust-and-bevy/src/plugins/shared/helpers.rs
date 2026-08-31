use bevy::{
    asset::AssetServer,
    ecs::{hierarchy::ChildOf, relationship::RelatedSpawnerCommands},
    math::Vec2,
    sprite::Sprite,
    transform::components::Transform,
    utils::default,
};

use crate::plugins::{BoxTexture, CORNER_BOX_TEXTURE_SIZE};

pub fn load_box_graphics(asset_server: &AssetServer, folder: &str) -> BoxTexture {
    let bottom = asset_server.load(format!("{}/bottom.png", folder));
    let bottom_left = asset_server.load(format!("{}/bottomleft.png", folder));
    let bottom_right = asset_server.load(format!("{}/bottomright.png", folder));
    let center = asset_server.load(format!("{}/center.png", folder));
    let left = asset_server.load(format!("{}/left.png", folder));
    let right = asset_server.load(format!("{}/right.png", folder));
    let top = asset_server.load(format!("{}/top.png", folder));
    let top_left = asset_server.load(format!("{}/topleft.png", folder));
    let top_right = asset_server.load(format!("{}/topright.png", folder));

    BoxTexture {
        bottom,
        bottom_left,
        bottom_right,
        center,
        left,
        right,
        top,
        top_left,
        top_right,
    }
}

/*
 * Visually, a single brick will be composed of several images which, when put together should create an image.
 * Think of it as a mosaic of pieces which together create a picture.
 */
pub fn spawn_box_texture_parts(
    parent: &mut RelatedSpawnerCommands<'_, ChildOf>,
    box_texture: &BoxTexture,
    box_size: Vec2,
) {
    let box_half_size = box_size / 2.;
    let corner_half_size = CORNER_BOX_TEXTURE_SIZE / 2.;
    let inner_line_size = Vec2::new(
        box_size.x - CORNER_BOX_TEXTURE_SIZE.x * 2.,
        box_size.y - CORNER_BOX_TEXTURE_SIZE.y * 2.,
    );

    // Spawn corners
    parent.spawn((
        Sprite::from_image(box_texture.top_left.clone()),
        Transform::from_xyz(
            -box_half_size.x + corner_half_size.x,
            box_half_size.y - corner_half_size.y,
            0.0,
        ),
    ));
    parent.spawn((
        Sprite::from_image(box_texture.top_right.clone()),
        Transform::from_xyz(
            inner_line_size.x / 2. + corner_half_size.x,
            box_half_size.y - corner_half_size.y,
            0.0,
        ),
    ));
    parent.spawn((
        Sprite::from_image(box_texture.bottom_left.clone()),
        Transform::from_xyz(
            -box_half_size.x + corner_half_size.x,
            -box_half_size.y + corner_half_size.y,
            0.0,
        ),
    ));
    parent.spawn((
        Sprite::from_image(box_texture.bottom_right.clone()),
        Transform::from_xyz(
            inner_line_size.x / 2. + corner_half_size.x,
            -box_half_size.y + corner_half_size.y,
            0.0,
        ),
    ));

    // Spawn edges (stretched with custom_size)
    parent.spawn((
        Sprite {
            image: box_texture.top.clone(),
            custom_size: Some(Vec2::new(inner_line_size.x, CORNER_BOX_TEXTURE_SIZE.y)),
            ..default()
        },
        Transform::from_xyz(0.0, box_half_size.y - corner_half_size.y, 0.0),
    ));
    parent.spawn((
        Sprite {
            image: box_texture.bottom.clone(),
            custom_size: Some(Vec2::new(inner_line_size.x, CORNER_BOX_TEXTURE_SIZE.y)),
            ..default()
        },
        Transform::from_xyz(0.0, -box_half_size.y + corner_half_size.y, 0.0),
    ));
    parent.spawn((
        Sprite {
            image: box_texture.left.clone(),
            custom_size: Some(Vec2::new(CORNER_BOX_TEXTURE_SIZE.x, inner_line_size.y)),
            ..default()
        },
        Transform::from_xyz(-box_half_size.x + corner_half_size.x, 0.0, 0.0),
    ));
    parent.spawn((
        Sprite {
            image: box_texture.right.clone(),
            custom_size: Some(Vec2::new(CORNER_BOX_TEXTURE_SIZE.x, inner_line_size.y)),
            ..default()
        },
        Transform::from_xyz(box_half_size.x - corner_half_size.x, 0.0, 0.0),
    ));

    // Spawn center (stretched with custom_size)
    parent.spawn((
        Sprite {
            image: box_texture.center.clone(),
            custom_size: Some(Vec2::new(inner_line_size.x, inner_line_size.y)),
            ..default()
        },
        Transform::from_xyz(0.0, 0.0, 0.0),
    ));
}
