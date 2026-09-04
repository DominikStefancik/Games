use bevy::{
    asset::AssetServer,
    camera::Camera2d,
    ecs::{
        query::Changed,
        system::{Commands, Query, Res},
    },
    math::{Vec2, Vec3},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BoxTextureParts, CORNER_BOX_TEXTURE_SIZE, Collider, UpgradeTexture, load_box_graphics,
    shared::GameTexture,
};

pub fn spawn_camera(mut commands: Commands) {
    commands.spawn(Camera2d);
}

pub fn load_textures(mut commands: Commands, asset_server: Res<AssetServer>) {
    let background = asset_server.load("graphics/other/background.png");
    let ball = asset_server.load("graphics/other/ball.png");
    let paddle = load_box_graphics(&asset_server, "graphics/paddle");
    let blue_brick = load_box_graphics(&asset_server, "graphics/bricks/blue");
    let bronze_brick = load_box_graphics(&asset_server, "graphics/bricks/bronze");
    let green_brick = load_box_graphics(&asset_server, "graphics/bricks/green");
    let grey_brick = load_box_graphics(&asset_server, "graphics/bricks/grey");
    let orange_brick = load_box_graphics(&asset_server, "graphics/bricks/orange");
    let purple_brick = load_box_graphics(&asset_server, "graphics/bricks/purple");
    let red_brick = load_box_graphics(&asset_server, "graphics/bricks/red");
    let upgrade = UpgradeTexture {
        heart: asset_server.load("graphics/upgrades/heart.png"),
        laser: asset_server.load("graphics/upgrades/laser.png"),
        size: asset_server.load("graphics/upgrades/size.png"),
        speed: asset_server.load("graphics/upgrades/speed.png"),
    };
    let heart = asset_server.load("graphics/other/heart.png");
    let laser = asset_server.load("graphics/other/laser.png");

    let game_texture = GameTexture {
        background,
        ball,
        paddle,
        blue_brick,
        bronze_brick,
        green_brick,
        grey_brick,
        orange_brick,
        purple_brick,
        red_brick,
        upgrade,
        heart,
        laser,
    };

    commands.insert_resource(game_texture);
}

/*
 * This system runs whenever Collider changes. We just mutate the component. We don't need a manual "resize" function
 * to touch every sprite ourselves.
 *
 * The query filter Query<..., Changed<Collider>> means the system iterates zero entities on frames where nothing changed —
 * Bevy's change detection tracks this per-component, so the query effectively skips straight past bricks that
 * haven't been touched. Scheduling it in Update every frame doesn't mean "recompute every box's geometry every frame" —
 * it means "check if any brick's size changed this frame, and only recompute those."
 * So we don't need to gate it behind an event or manually call it only when resizing happens;
 * that's exactly what Changed<T> is for.
 */
pub fn apply_box_texture_resize(
    box_texture_parts_query: Query<(&Collider, &BoxTextureParts), Changed<Collider>>,
    mut transform_query: Query<&mut Transform>,
    mut sprite_query: Query<&mut Sprite>,
) {
    for (collider, parts) in &box_texture_parts_query {
        let box_half_size = collider.size / 2.;
        let corner_half_size = CORNER_BOX_TEXTURE_SIZE / 2.;
        let inner_line_size = Vec2::new(
            collider.size.x - CORNER_BOX_TEXTURE_SIZE.x * 2.,
            collider.size.y - CORNER_BOX_TEXTURE_SIZE.y * 2.,
        );

        // Corners (reposition only, size stays fixed)
        transform_query.get_mut(parts.top_left).unwrap().translation = Vec3::new(
            -box_half_size.x + corner_half_size.x,
            box_half_size.y - corner_half_size.y,
            0.0,
        );
        transform_query
            .get_mut(parts.top_right)
            .unwrap()
            .translation = Vec3::new(
            inner_line_size.x / 2. + corner_half_size.x,
            box_half_size.y - corner_half_size.y,
            0.0,
        );
        transform_query
            .get_mut(parts.bottom_left)
            .unwrap()
            .translation = Vec3::new(
            -box_half_size.x + corner_half_size.x,
            -box_half_size.y + corner_half_size.y,
            0.0,
        );
        transform_query
            .get_mut(parts.bottom_right)
            .unwrap()
            .translation = Vec3::new(
            inner_line_size.x / 2. + corner_half_size.x,
            -box_half_size.y + corner_half_size.y,
            0.0,
        );

        // Edges (reposition + resize/stretch with custom_size)
        transform_query.get_mut(parts.top).unwrap().translation =
            Vec3::new(0.0, box_half_size.y - corner_half_size.y, 0.0);
        sprite_query.get_mut(parts.top).unwrap().custom_size =
            Some(Vec2::new(inner_line_size.x, CORNER_BOX_TEXTURE_SIZE.y));

        transform_query.get_mut(parts.bottom).unwrap().translation =
            Vec3::new(0.0, -box_half_size.y + corner_half_size.y, 0.0);
        sprite_query.get_mut(parts.bottom).unwrap().custom_size =
            Some(Vec2::new(inner_line_size.x, CORNER_BOX_TEXTURE_SIZE.y));

        transform_query.get_mut(parts.left).unwrap().translation =
            Vec3::new(-box_half_size.x + corner_half_size.x, 0.0, 0.0);
        sprite_query.get_mut(parts.left).unwrap().custom_size =
            Some(Vec2::new(CORNER_BOX_TEXTURE_SIZE.x, inner_line_size.y));

        transform_query.get_mut(parts.right).unwrap().translation =
            Vec3::new(box_half_size.x - corner_half_size.x, 0.0, 0.0);
        sprite_query.get_mut(parts.right).unwrap().custom_size =
            Some(Vec2::new(CORNER_BOX_TEXTURE_SIZE.x, inner_line_size.y));

        // Center (resize/stretch with custom_size)
        transform_query.get_mut(parts.center).unwrap().translation = Vec3::new(0.0, 0.0, 0.0);
        sprite_query.get_mut(parts.center).unwrap().custom_size =
            Some(Vec2::new(inner_line_size.x, inner_line_size.y));
    }
}
