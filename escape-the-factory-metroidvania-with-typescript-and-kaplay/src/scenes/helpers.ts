import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import type { RoomData, TiledObject } from "./models";
import {
  ANIMATION,
  COLLIDER_TYPE,
  MAP_HORIZONTAL_OFFSET,
  TAG,
} from "../constants";
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
      const bossBarrier = map.add([
        kaplayContext.rect(collider.width, collider.height),
        kaplayContext.Color.fromHex("#eacfba"),
        kaplayContext.pos(collider.x, collider.y),
        kaplayContext.area({ collisionIgnore: [TAG.collider] }),
        kaplayContext.opacity(0),
        TAG["boss-barrier"],
        {
          activate(this: GameObj) {
            // we change the opacity of the barrier
            kaplayContext.tween(
              this.opacity,
              0.3,
              1,
              (newValue) => (this.opacity = newValue),
              kaplayContext.easings.linear,
            );

            if (collider.properties) {
              // and then move the camera to center it to the area where a boss is
              kaplayContext.tween(
                kaplayContext.getCamPos().x,
                collider.properties[0].value,
                1,
                (newValue) =>
                  kaplayContext.setCamPos(
                    newValue,
                    kaplayContext.getCamPos().y,
                  ),
                kaplayContext.easings.linear,
              );
            }
          },
          async deactivate(this: GameObj, playerPosX: number) {
            // we change the opacity of the barrier so it dissappers
            kaplayContext.tween(
              this.opacity,
              0,
              1,
              (newValue) => (this.opacity = newValue),
              kaplayContext.easings.linear,
            );

            // and then move the camera to the players position
            await kaplayContext.tween(
              kaplayContext.getCamPos().x,
              playerPosX,
              1,
              (newValue) =>
                kaplayContext.setCamPos(newValue, kaplayContext.getCamPos().y),
              kaplayContext.easings.linear,
            );

            kaplayContext.destroy(this);
          },
        },
      ]);

      bossBarrier.onCollide(TAG.player, async (player: GameObj) => {
        const currentState = state.getState();

        if (currentState.isPlayerInFightWithBoss) {
          return;
        }

        if (currentState.isBossDefeated) {
          state.setState("isPlayerInFightWithBoss", false);
          bossBarrier.deactivate(player.pos.x);
          return;
        }

        // if the player collides with the boss barrier, we want to make sure he is "sucked"
        // into the fighting area where the boss is
        //
        // so we firts make sure he cannot escape the colision
        player.disableControls();
        player.play(ANIMATION.player.idle);

        // then we move the player into the fighting area
        await kaplayContext.tween(
          player.pos.x,
          player.pos.x + 25,
          0.3,
          (newValue) => (player.pos.x = newValue),
          kaplayContext.easings.linear,
        );

        // after the player is in the area, we make sure he can fight
        player.setControls();
      });

      bossBarrier.onCollideEnd(TAG.player, () => {
        const currentState = state.getState();

        if (
          currentState.isPlayerInFightWithBoss ||
          currentState.isBossDefeated
        ) {
          return;
        }

        state.setState("isPlayerInFightWithBoss", true);
        bossBarrier.activate();
        bossBarrier.use(kaplayContext.body({ isStatic: true }));
      });

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
