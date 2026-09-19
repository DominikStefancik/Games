use bevy::ecs::{
    entity::Entity,
    query::With,
    system::{Commands, Query, Res, SystemParam},
};

use crate::plugins::{
    BallQuery, Brick, Heart, Laser, MovingArea, PADDLE_INITIAL_SIZE, PaddleQuery, Projectile,
    Upgrade, get_ball_initial_position, get_paddle_initial_position,
};

/*
 * SystemParam is the trait that answers "what is a system allowed to take as an argument?" and, just as importantly,
 * "what data does this system touch?" so the scheduler can decide what may run in parallel.
 *
 * The reason why we have to use two lifetimes:
 *      Single<'w, 's, D, F> and Query<'w, 's, D, F> carry:
 *
 *          'w — the borrow of the world (the actual component data)
 *          's — the borrow of the param's own cached state
 *
 *      They're separate because the state outlives any single run: it's created once at init_state and reused every frame,
 *      while the world borrow lasts only for that run. Item<'world, 'state> is where the two get bound together —
 *      the doc comment says it should be "Self, instantiated with new lifetimes."
 */
#[derive(SystemParam)]
pub struct GameEntities<'w, 's> {
    pub commands: Commands<'w, 's>,
    moving_area: Res<'w, MovingArea>,
    ball_query: BallQuery<'w, 's>,
    paddle_query: PaddleQuery<'w, 's>,
    pub brick_query: Query<'w, 's, Entity, With<Brick>>,
    heart_query: Query<'w, 's, (Entity, &'static Heart)>,
    laser_query: Query<'w, 's, Entity, With<Laser>>,
    projectile_query: Query<'w, 's, Entity, With<Projectile>>,
    upgrade_query: Query<'w, 's, Entity, With<Upgrade>>,
}

impl GameEntities<'_, '_> {
    pub fn reset_moving_elements(&mut self) {
        /*
         * Using "&mut *self.ball_query" replaces ball_query.into_inner().
         * into_inner() consumes the Single, which we can't do from "&mut self".
         * DerefMut gives us the item tuple to destructure in place.
         */
        let (ball_transform, ball) = &mut *self.ball_query;
        let (paddle_transform, paddle_collider, paddle) = &mut *self.paddle_query;

        ball.reset();
        ball_transform.translation = get_ball_initial_position(&self.moving_area);

        paddle.reset();
        paddle_collider.size = PADDLE_INITIAL_SIZE;
        paddle_transform.translation = get_paddle_initial_position();

        for entity in self
            .laser_query
            .iter()
            .chain(&self.projectile_query)
            .chain(&self.upgrade_query)
        {
            self.commands.entity(entity).despawn();
        }
    }

    pub fn reset_ball(&mut self) {
        /*
         * Using "&mut *self.ball_query" replaces ball_query.into_inner().
         * into_inner() consumes the Single, which we can't do from "&mut self".
         * DerefMut gives us the item tuple to destructure in place.
         */
        let (_, ball) = &mut *self.ball_query;
        ball.reset();
    }

    pub fn despawn_bricks(&mut self) {
        for brick_entity in &self.brick_query {
            self.commands.entity(brick_entity).despawn();
        }
    }

    pub fn despawn_all_hearts(&mut self) {
        for (heart_entity, _) in &self.heart_query {
            self.commands.entity(heart_entity).despawn();
        }
    }

    pub fn despawn_heart(&mut self, index: u16) {
        for (heart_entity, heart) in &self.heart_query {
            if heart.index == index {
                self.commands.entity(heart_entity).despawn();
            }
        }
    }
}
