use bevy::{
    ecs::{
        query::{With, Without},
        system::Single,
    },
    transform::components::Transform,
};

use crate::plugins::{Ball, Collider, Paddle};

/*
 * Single has two lifetimes in Bevy 0.19:
 *      pub struct Single<'w, 's, D: IterQueryData, F: QueryFilter = ()>
 *          'w — the borrow of the world (the actual component data)
 *          's — the borrow of the query's own cached state
 *
 * The component references inside D must be &'static mut T, not &'w mut T.
 * D is a marker type. The real borrow lifetimes are produced by QueryData::Item<'w, 's>,
 * which Single binds from its own 'w/'s.
 * IntoSystem/IntoObserver need the function to be generic over all lifetimes (a higher-ranked bound).
 * Writing &'w mut Transform pins D to one specific lifetime, the Higher-Rank Trait Bounds (HRTB) no longer holds,
 * and the function stops being a system.
 *
 * 'static here is just the conventional placeholder in a type-level marker — it does NOT mean the borrow lives forever
 * -> the real borrows come from 'w/'s on the wrapper.
 */
pub type BallQuery<'w, 's> =
    Single<'w, 's, (&'static mut Transform, &'static mut Ball), (With<Ball>, Without<Paddle>)>;

pub type PaddleQuery<'w, 's> = Single<
    'w,
    's,
    (
        &'static mut Transform,
        &'static mut Collider,
        &'static mut Paddle,
    ),
    (With<Paddle>, Without<Ball>),
>;
