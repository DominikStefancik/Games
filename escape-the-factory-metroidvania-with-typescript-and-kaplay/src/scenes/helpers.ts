import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import type { RoomData, TiledObject } from "./models";
import { COLLIDER_TYPE, MAP_HORIZONTAL_OFFSET, TAG } from "../constants";
import { state } from "../state/globalStateManager";

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
        kaplayContext.body({ isStatic: true }),
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

export const setCameraHorizontalControls = (params: {
  player: GameObj;
  map: GameObj;
  roomData: RoomData;
}) => {
  const { player, map, roomData } = params;

  kaplayContext.onUpdate(() => {
    const { x: playerX } = player.pos;
    const { x: mapX } = map.pos;
    const { y: cameraY } = kaplayContext.getCamPos();

    // if the player is in a fight with a level boss, we don't want the camera to move
    if (state.getState().isPlayerInFightWithBoss) {
      return;
    }

    // don't go too much of the left part of the map
    if (mapX + MAP_HORIZONTAL_OFFSET > playerX) {
      kaplayContext.setCamPos(mapX + MAP_HORIZONTAL_OFFSET, cameraY);
      return;
    }

    if (
      playerX >
      mapX + roomData.width * roomData.tilewidth - MAP_HORIZONTAL_OFFSET
    ) {
      kaplayContext.setCamPos(
        mapX + roomData.width * roomData.tilewidth - MAP_HORIZONTAL_OFFSET,
        cameraY,
      );
      return;
    }

    // camera will follow the player position
    kaplayContext.setCamPos(playerX, cameraY);
  });
};

export const setCameraVerticalZones = (
  map: GameObj,
  cameras: TiledObject[],
) => {
  for (const camera of cameras) {
    /*
     * Add to the map an invisible object representing "a boundary" of a camera cameraZone
     * this object will then serve for deciding if the camera should move
     * by detecting a collision with the player (see the code below)
     */
    const cameraZone = map.add([
      kaplayContext.pos(camera.x, camera.y),
      kaplayContext.area({
        shape: new kaplayContext.Rect(
          kaplayContext.vec2(0),
          camera.width,
          camera.height,
        ),
        collisionIgnore: [TAG.collider],
      }),
    ]);

    /*
     * Whenever a player collides with an invisible object representing "a boundary" of a camera cameraZone
     * move the camera vertically by using the "tween" method
     *
     * the method "onCollide" is available on a game object which have the "area" component
     */
    cameraZone.onCollide(TAG.player, () => {
      if (camera.properties) {
        // the "properties" array represents a set custom custom properties defined in the room1.json  and room2.json
        // in our game the "camera" type object have only one custom property
        const camerCustomProperty = camera.properties[0].value;

        if (kaplayContext.getCamPos().x !== camerCustomProperty) {
          const { x, y } = kaplayContext.getCamPos();

          kaplayContext.tween(
            y,
            camerCustomProperty,
            0.8,
            (newValue) => kaplayContext.setCamPos(x, newValue),
            kaplayContext.easings.linear,
          );
        }
      }
    });
  }
};
