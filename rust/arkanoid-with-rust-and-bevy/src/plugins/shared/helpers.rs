use bevy::{
    asset::AssetServer,
    ecs::{hierarchy::ChildOf, relationship::RelatedSpawnerCommands},
    math::bounding::{Aabb2d, IntersectsVolume},
    sprite::Sprite,
};

use crate::plugins::{BoxTexture, BoxTextureParts};

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
) -> Option<BoxTextureParts> {
    /*
     * Storing the child Entity IDs directly (rather than re-discovering them via Children + queries every time)
     * means the resize system doesn't need to guess which child is which — it just writes straight to each one.
     */

    // Spawn corners
    let top_left = parent
        .spawn(Sprite::from_image(box_texture.top_left.clone()))
        .id();
    let top_right = parent
        .spawn(Sprite::from_image(box_texture.top_right.clone()))
        .id();
    let bottom_left = parent
        .spawn(Sprite::from_image(box_texture.bottom_left.clone()))
        .id();
    let bottom_right = parent
        .spawn(Sprite::from_image(box_texture.bottom_right.clone()))
        .id();

    // Spawn edges
    let top = parent
        .spawn(Sprite::from_image(box_texture.top.clone()))
        .id();
    let bottom = parent
        .spawn(Sprite::from_image(box_texture.bottom.clone()))
        .id();
    let left = parent
        .spawn(Sprite::from_image(box_texture.left.clone()))
        .id();
    let right = parent
        .spawn(Sprite::from_image(box_texture.right.clone()))
        .id();

    // Spawn center
    let center = parent
        .spawn(Sprite::from_image(box_texture.center.clone()))
        .id();

    Some(BoxTextureParts {
        top_left,
        top_right,
        bottom_left,
        bottom_right,
        left,
        right,
        top,
        bottom,
        center,
    })
}

pub fn detect_rectangle_collision(
    upgrade_bounding_rectangle: Aabb2d,
    paddle_bounding_rectangle: Aabb2d,
) -> bool {
    upgrade_bounding_rectangle.intersects(&paddle_bounding_rectangle)
}
