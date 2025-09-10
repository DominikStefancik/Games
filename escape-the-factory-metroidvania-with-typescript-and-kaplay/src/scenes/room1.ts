import {
  MAP_SPRITE,
  POSITION_TAG,
  ROOM_DATA_LAYER_NAME,
  SCENE,
  VERTICAL_BOUND,
} from "../constants";
import { createEnemyBoss } from "../entities/enemyBoss";
import { createEnemyDrone } from "../entities/enemyDrone";
import { createHealthCartridge } from "../entities/healthCartridge";
import { createPlayer } from "../entities/player";
import kaplayContext from "../kaplay-context";
import { stateManager } from "../state/globalStateManager";
import { healthBar } from "../ui/healthBar";
import {
  setBackground,
  setCameraHorizontalControls,
  setCameraVerticalZones,
  setMapColliders,
} from "./helpers";
import type { RoomData } from "./models";

export const room1 = (roomData: RoomData) => {
  setBackground("#a2aed5");

  kaplayContext.setCamScale(4);
  kaplayContext.setCamPos(170, 100);
  kaplayContext.setGravity(1000);

  // method "add()" from Kaplay creates a game object and makes it visible in a scene
  // whereas the method "make()" from Kaplay just creates a game object, but doesn't make it visible
  //
  // the "map" game object will be a parent of everything and then its child game objects will be positioned
  // relatively to the "map" object
  const map = kaplayContext.add([
    kaplayContext.sprite(MAP_SPRITE.room1),
    kaplayContext.pos(),
  ]);

  const colliders = [];
  const positions = [];
  const cameras = [];

  for (const layer of roomData.layers) {
    switch (layer.name) {
      case ROOM_DATA_LAYER_NAME.colliders:
        colliders.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.positions:
        positions.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.cameras:
        cameras.push(...layer.objects);
        break;
      default:
        break;
    }
  }

  setMapColliders(map, colliders);
  setCameraVerticalZones(map, cameras);

  for (const position of positions) {
    if (position.name === POSITION_TAG.player) {
      const player = map.add(createPlayer());
      player.setPosition(kaplayContext.vec2(position.x, position.y));
      player.setControls();
      player.setEvents();
      player.respawnIfOutOfBounds(VERTICAL_BOUND.room1, SCENE.room1);
      setCameraHorizontalControls({ map, player, roomData });
    }

    if (position.type === POSITION_TAG.drone) {
      const drone = map.add(
        createEnemyDrone(kaplayContext.vec2(position.x, position.y)),
      );
      drone.setBehaviour();
      drone.setEvents();
    }

    if (
      position.name === POSITION_TAG.boss &&
      !stateManager.getState().isBossDefeated
    ) {
      const boss = map.add(
        createEnemyBoss(kaplayContext.vec2(position.x, position.y)),
      );
      boss.setBehaviour();
      boss.setEvents();
    }

    if (position.type === POSITION_TAG.cartridge) {
      map.add(
        createHealthCartridge(kaplayContext.vec2(position.x, position.y)),
      );
    }
  }

  kaplayContext.add(healthBar);
};
