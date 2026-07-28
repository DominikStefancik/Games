use bevy::{
    color::Alpha,
    ecs::{
        entity::{ContainsEntity, Entity},
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    math::{Vec2, Vec3},
    sprite::Sprite,
    time::{Time, Timer, TimerMode},
    transform::components::Transform,
};
use rand::RngExt;

use crate::{
    core::{Grid, PARTICLE_COLOR, Randomizer},
    plugins::{
        food::{Food, FoodParticle, FoodSprite, new_food_position, render_food},
        shared::{FoodConsumed, GameStartTriggered},
        snake::Snake,
    },
};

pub fn initialise_food(
    _: On<GameStartTriggered>,
    mut commands: Commands,
    randomizer: ResMut<Randomizer>,
    grid: Res<Grid>,
    snake: ResMut<Snake>,
    mut food: ResMut<Food>,
) {
    let position = new_food_position(randomizer.into_inner(), &grid, &snake);
    food.0 = position;

    render_food(&mut commands, &grid, &food);
}

pub fn create_new_food(
    _: On<FoodConsumed>,
    mut commands: Commands,
    randomizer: ResMut<Randomizer>,
    grid: Res<Grid>,
    snake: ResMut<Snake>,
    mut food: ResMut<Food>,
    food_sprite: Single<Entity, With<FoodSprite>>,
) {
    let position = new_food_position(randomizer.into_inner(), &grid, &snake);
    food.0 = position;

    commands.entity(food_sprite.entity()).despawn();
    render_food(&mut commands, &grid, &food);
}

pub fn spawn_food_particles(
    _: On<FoodConsumed>,
    mut commands: Commands,
    mut randomizer: ResMut<Randomizer>,
    grid: Res<Grid>,
    food: Res<Food>,
) {
    for _ in 1..10 {
        /*
         * TAU is 2π, a full circle in radians. Multiplying a random float by TAU gives a random angle.
         * angle.cos() and angle.sin() give the x and y components of a unit vector in that direction, scaled by speed.
         * Each particle gets its own lifetime timer.
         * This is why Particle is a component rather than a resource, many particles can exist simultaneously,
         * each with independent state.
         */
        let angle = randomizer.rng.random::<f32>() * std::f32::consts::TAU;
        let speed = 3. + randomizer.rng.random::<f32>() * 4.;

        commands.spawn((
            FoodParticle {
                velocity: Vec2::new(angle.cos() * speed, angle.sin() * speed),
                timer: Timer::from_seconds(0.6, TimerMode::Once),
            },
            Sprite::from_color(PARTICLE_COLOR, Vec2::splat(5.)),
            Transform::from_translation(grid.to_pixels(food.0, 0.)),
        ));
    }
}

pub fn update_particles(
    mut commands: Commands,
    time: Res<Time>,
    particles_query: Query<(Entity, &mut FoodParticle, &mut Transform, &mut Sprite)>,
) {
    for (entity, mut particle, mut transform, mut sprite) in particles_query {
        particle.timer.tick(time.delta());

        if particle.timer.is_finished() {
            commands.entity(entity).despawn();
            continue;
        }

        /*
         * fraction_remaining goes from 1.0 to 0.0 as the particle ages. Alpha fades from 1.0 to 0.0.
         * Scale goes from 0.5 + 1.0 * 0.5 = 1.0 down to 0.5 + 0.0 * 0.5 = 0.5,
         * so particles shrink slightly as they die.
         */
        let fraction_remaining = particle.timer.fraction_remaining();
        transform.translation.x += particle.velocity.x + time.delta_secs();
        transform.translation.y += particle.velocity.y + time.delta_secs();
        sprite.color.set_alpha(fraction_remaining);
        transform.scale = Vec3::splat(0.5 + fraction_remaining * 0.5);
    }
}
