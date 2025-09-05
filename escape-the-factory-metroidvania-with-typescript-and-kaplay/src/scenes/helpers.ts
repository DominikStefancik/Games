import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import type { TiledObject } from "./models";
import { COLLIDER_TYPE, TAG } from "../constants";

export const setBackground = (hexColorCode: string) => {
  kaplayContext.add([
    kaplayContext.rect(kaplayContext.width(), kaplayContext.height()),
    kaplayContext.color(kaplayContext.Color.fromHex(hexColorCode)),
    // the background will stay fixed and will not move as the camera moves
    kaplayContext.fixed(),
    // if we don't specify the "pos()" component, Kaplay will automaticaly position the game object
    // to the (0, 0) position
  ]);
};

export const setMapColliders = (map: GameObj, colliders: TiledObject[]) => {
  for (const collider of colliders) {
    if (collider.polygon) {
      const coordinates = [];

      for (const point of collider.polygon) {
        coordinates.push(kaplayContext.vec2(point.x, point.y));
      }

      map.add([
        kaplayContext.pos(collider.x, collider.y),
        kaplayContext.area({
          shape: new kaplayContext.Polygon(coordinates),
          collisionIgnore: [TAG.collider],
        }),
        TAG.collider,
        // a game object can have more than one tag
        // if a tag is an string, it is not considered as tag
        collider.type,
      ]);

      continue;
    }

    if (collider.name === COLLIDER_TYPE["boss-barrier"]) {
      const bossBarrier = map.add([]);

      continue;
    }

    map.add([
      kaplayContext.pos(collider.x, collider.y),
      kaplayContext.area({
        // "shape" property only adds a rectangular hitbox to the "map" game object, but it will NOT draw a rectangle
        shape: new kaplayContext.Rect(
          kaplayContext.vec2(0),
          collider.width,
          collider.height,
        ),
        collisionIgnore: [TAG.collider],
      }),
      // the "body" component can be defind ONLY when a game object has also the "area" component
      // the property "isStatic" makes sure that a game object will not move if it collides with another game object
      kaplayContext.body({ isStatic: true }),
      TAG.collider,
    ]);
  }
};
